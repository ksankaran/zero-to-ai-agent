# From: AI Agents Book, Chapter 18, Section 18.2
# File: exercise_3_18_2_solution.py
# Description: Exercise 3 Solution - FAQ agent with context maintenance

import pytest
from unittest.mock import MagicMock
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


class FAQState(TypedDict):
    messages: Annotated[list, add_messages]
    topics_discussed: list[str]
    current_topic: str | None


def detect_topic(message: str, previous_topics: list[str]) -> str:
    """Detect the topic of a message, considering context."""
    message_lower = message.lower()
    
    # Direct topic mentions
    if "pricing" in message_lower or "cost" in message_lower or "price" in message_lower:
        return "pricing"
    elif "shipping" in message_lower or "delivery" in message_lower:
        return "shipping"
    elif "return" in message_lower or "refund" in message_lower:
        return "returns"
    elif "discount" in message_lower or "coupon" in message_lower or "sale" in message_lower:
        # Context-aware: "discount" after "pricing" is about pricing discounts
        if "pricing" in previous_topics:
            return "pricing"
        return "discounts"
    elif "hours" in message_lower or "open" in message_lower:
        return "hours"
    
    # If no direct match, continue previous topic
    if previous_topics:
        return previous_topics[-1]
    
    return "general"


def answer_question(state: FAQState, llm) -> dict:
    """Generate an answer based on topic and context."""
    messages = state["messages"]
    last_message = messages[-1].content
    topics_discussed = state.get("topics_discussed", [])
    
    # Detect topic with context awareness
    topic = detect_topic(last_message, topics_discussed)
    
    # Build context-aware prompt
    context = ""
    if topics_discussed:
        context = f"Previously discussed topics: {', '.join(topics_discussed)}. "
    
    prompt = f"{context}User question about {topic}: {last_message}"
    
    response = llm.invoke([
        SystemMessage(content=f"You are answering a question about {topic}."),
        HumanMessage(content=prompt)
    ])
    
    # Update topics discussed
    new_topics = topics_discussed.copy()
    if topic not in new_topics:
        new_topics.append(topic)
    
    return {
        "messages": [AIMessage(content=response.content)],
        "topics_discussed": new_topics,
        "current_topic": topic
    }


def build_faq_graph(llm):
    """Build the FAQ agent graph."""
    graph = StateGraph(FAQState)
    
    graph.add_node("answer", lambda s: answer_question(s, llm))
    
    graph.add_edge(START, "answer")
    graph.add_edge("answer", END)
    
    return graph.compile()


# Integration tests
class TestFAQContextMaintenance:
    """Integration tests for FAQ context maintenance."""
    
    @pytest.fixture
    def mock_llm(self):
        """Create a mock LLM that echoes the topic."""
        llm = MagicMock()
        # Return response that includes topic for verification
        def dynamic_response(messages):
            # Extract topic from system message
            system_msg = next((m for m in messages if isinstance(m, SystemMessage)), None)
            topic = "unknown"
            if system_msg:
                topic = system_msg.content.split("about ")[-1].rstrip(".")
            return MagicMock(content=f"Here's information about {topic}")
        
        llm.invoke.side_effect = dynamic_response
        return llm
    
    def test_first_question_starts_fresh_context(self, mock_llm):
        """Test that first question has no prior context."""
        graph = build_faq_graph(mock_llm)
        
        initial_state = {
            "messages": [HumanMessage(content="What is your pricing?")],
            "topics_discussed": [],
            "current_topic": None
        }
        
        result = graph.invoke(initial_state)
        
        assert result["current_topic"] == "pricing"
        assert "pricing" in result["topics_discussed"]
        assert len(result["topics_discussed"]) == 1
    
    def test_context_maintained_across_questions(self, mock_llm):
        """Test that context accumulates across questions."""
        graph = build_faq_graph(mock_llm)
        
        # First question about pricing
        state_1 = {
            "messages": [HumanMessage(content="What is your pricing?")],
            "topics_discussed": [],
            "current_topic": None
        }
        result_1 = graph.invoke(state_1)
        
        assert result_1["current_topic"] == "pricing"
        assert result_1["topics_discussed"] == ["pricing"]
        
        # Second question - simulate continuing conversation
        state_2 = {
            "messages": result_1["messages"] + [HumanMessage(content="What about shipping?")],
            "topics_discussed": result_1["topics_discussed"],
            "current_topic": result_1["current_topic"]
        }
        result_2 = graph.invoke(state_2)
        
        assert result_2["current_topic"] == "shipping"
        assert "pricing" in result_2["topics_discussed"]
        assert "shipping" in result_2["topics_discussed"]
    
    def test_discount_question_uses_pricing_context(self, mock_llm):
        """Test that 'discounts' after 'pricing' stays in pricing context."""
        graph = build_faq_graph(mock_llm)
        
        # First establish pricing context
        state_1 = {
            "messages": [HumanMessage(content="What are your prices?")],
            "topics_discussed": [],
            "current_topic": None
        }
        result_1 = graph.invoke(state_1)
        
        # Now ask about discounts - should relate to pricing
        state_2 = {
            "messages": result_1["messages"] + [HumanMessage(content="Any discounts available?")],
            "topics_discussed": result_1["topics_discussed"],
            "current_topic": result_1["current_topic"]
        }
        result_2 = graph.invoke(state_2)
        
        # Because pricing was discussed, discount should be treated as pricing-related
        assert result_2["current_topic"] == "pricing"
    
    def test_discount_question_without_context(self, mock_llm):
        """Test that 'discounts' without context is its own topic."""
        graph = build_faq_graph(mock_llm)
        
        # Ask about discounts first (no pricing context)
        initial_state = {
            "messages": [HumanMessage(content="Do you have any discounts?")],
            "topics_discussed": [],
            "current_topic": None
        }
        
        result = graph.invoke(initial_state)
        
        # Without pricing context, should be its own topic
        assert result["current_topic"] == "discounts"
    
    def test_ambiguous_followup_uses_previous_topic(self, mock_llm):
        """Test that ambiguous follow-ups use the previous topic."""
        graph = build_faq_graph(mock_llm)
        
        # Establish shipping topic
        state_1 = {
            "messages": [HumanMessage(content="How does shipping work?")],
            "topics_discussed": [],
            "current_topic": None
        }
        result_1 = graph.invoke(state_1)
        
        # Ask ambiguous follow-up
        state_2 = {
            "messages": result_1["messages"] + [HumanMessage(content="What about international?")],
            "topics_discussed": result_1["topics_discussed"],
            "current_topic": result_1["current_topic"]
        }
        result_2 = graph.invoke(state_2)
        
        # Should continue with shipping topic
        assert result_2["current_topic"] == "shipping"
    
    def test_messages_preserved_through_conversation(self, mock_llm):
        """Test that all messages are preserved in conversation."""
        graph = build_faq_graph(mock_llm)
        
        # Build up a multi-turn conversation
        state = {
            "messages": [HumanMessage(content="Question 1: What are your hours?")],
            "topics_discussed": [],
            "current_topic": None
        }
        result = graph.invoke(state)
        
        # Add second question
        state = {
            "messages": result["messages"] + [HumanMessage(content="Question 2: What about weekends?")],
            "topics_discussed": result["topics_discussed"],
            "current_topic": result["current_topic"]
        }
        result = graph.invoke(state)
        
        # All messages should be present
        all_content = " ".join(m.content for m in result["messages"])
        assert "Question 1" in all_content
        assert "Question 2" in all_content
        
        # Should have both user questions and AI responses
        human_messages = [m for m in result["messages"] if isinstance(m, HumanMessage)]
        ai_messages = [m for m in result["messages"] if isinstance(m, AIMessage)]
        
        assert len(human_messages) == 2
        assert len(ai_messages) == 2
