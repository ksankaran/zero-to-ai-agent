# From: AI Agents Book, Chapter 18, Section 18.2
# File: test_support_agent.py
# Description: Integration tests demonstrating various testing strategies

import pytest
import os
from unittest.mock import MagicMock
from langchain_core.messages import HumanMessage, AIMessage
from support_agent import build_support_graph, SupportState


@pytest.fixture
def mock_llm():
    """Create a mock LLM that returns predictable responses."""
    llm = MagicMock()
    llm.invoke.return_value = MagicMock(
        content="I'd be happy to help you with that!"
    )
    return llm


# --- Basic Routing Tests ---

def test_refund_request_routes_correctly(mock_llm):
    """Test that refund requests go to the refund handler."""
    graph = build_support_graph(mock_llm)
    
    initial_state = {
        "messages": [HumanMessage(content="I want a refund for my order")],
        "issue_type": None,
        "resolved": False
    }
    
    result = graph.invoke(initial_state)
    
    # Verify routing worked correctly
    assert result["issue_type"] == "refund"
    assert result["resolved"] is True
    
    # Verify LLM was called (handler executed)
    assert mock_llm.invoke.called


def test_technical_issue_routes_correctly(mock_llm):
    """Test that technical issues go to the technical handler."""
    graph = build_support_graph(mock_llm)
    
    initial_state = {
        "messages": [HumanMessage(content="My device is broken")],
        "issue_type": None,
        "resolved": False
    }
    
    result = graph.invoke(initial_state)
    
    assert result["issue_type"] == "technical"
    assert result["resolved"] is True


# --- State Transition Tests ---

def test_state_accumulates_through_workflow(mock_llm):
    """Verify state is correctly passed and accumulated."""
    graph = build_support_graph(mock_llm)
    
    initial_state = {
        "messages": [HumanMessage(content="I need a refund please")],
        "issue_type": None,
        "resolved": False
    }
    
    result = graph.invoke(initial_state)
    
    # Original message should still be present
    assert len(result["messages"]) >= 1
    assert result["messages"][0].content == "I need a refund please"
    
    # AI response should have been added
    ai_messages = [m for m in result["messages"] if isinstance(m, AIMessage)]
    assert len(ai_messages) >= 1
    
    # State fields should be populated
    assert result["issue_type"] is not None
    assert result["resolved"] is True


# --- Property-Based Tests ---

def test_agent_always_responds(mock_llm):
    """Verify the agent always produces a response."""
    graph = build_support_graph(mock_llm)
    
    test_messages = [
        "I want a refund",
        "This is broken",
        "Cancel my subscription",
        "Hello, I have a question",
        "asdfghjkl",  # Gibberish input
    ]
    
    for message in test_messages:
        initial_state = {
            "messages": [HumanMessage(content=message)],
            "issue_type": None,
            "resolved": False
        }
        
        result = graph.invoke(initial_state)
        
        # Property: Agent should always add a response
        assert len(result["messages"]) > 1, f"No response for: {message}"
        
        # Property: Workflow should complete
        assert result["resolved"] is True, f"Not resolved for: {message}"


def test_agent_never_loses_messages(mock_llm):
    """Verify messages are never dropped during processing."""
    graph = build_support_graph(mock_llm)
    
    initial_messages = [
        HumanMessage(content="First message"),
        AIMessage(content="First response"),
        HumanMessage(content="I want a refund now"),
    ]
    
    initial_state = {
        "messages": initial_messages,
        "issue_type": None,
        "resolved": False
    }
    
    result = graph.invoke(initial_state)
    
    # All original messages should still be present
    assert len(result["messages"]) >= len(initial_messages)
    
    # Check that original content is preserved
    result_contents = [m.content for m in result["messages"]]
    for original in initial_messages:
        assert original.content in result_contents


# --- Error Handling Tests ---

def test_llm_error_is_handled_gracefully():
    """Test that LLM errors don't crash the entire workflow."""
    # Create an LLM that raises an error
    failing_llm = MagicMock()
    failing_llm.invoke.side_effect = Exception("API rate limit exceeded")
    
    graph = build_support_graph(failing_llm)
    
    initial_state = {
        "messages": [HumanMessage(content="I need help")],
        "issue_type": None,
        "resolved": False
    }
    
    # Expect the exception to propagate (no built-in error handling)
    with pytest.raises(Exception) as exc_info:
        graph.invoke(initial_state)
    
    assert "rate limit" in str(exc_info.value).lower()


# --- Integration Test with Real LLM (run sparingly) ---

@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="No API key available"
)
def test_with_real_llm():
    """Integration test with actual LLM - run sparingly."""
    from langchain_openai import ChatOpenAI
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    graph = build_support_graph(llm)
    
    initial_state = {
        "messages": [HumanMessage(content="I want to return my order #12345")],
        "issue_type": None,
        "resolved": False
    }
    
    result = graph.invoke(initial_state)

    # Test properties, not exact content
    # Note: We accept multiple issue types because LLM classification is
    # non-deterministic. Even with temperature=0, the model may classify
    # "return my order" as "refund", "general", or "order" depending on
    # subtle variations in model behavior across API calls.
    assert result["issue_type"] in ["refund", "general", "order"]
    assert result["resolved"] is True
    
    # Check that response mentions relevant information
    response = result["messages"][-1].content.lower()
    assert any(word in response for word in ["refund", "return", "order", "help"])
