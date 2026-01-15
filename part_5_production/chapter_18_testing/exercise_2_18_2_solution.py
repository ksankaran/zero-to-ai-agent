# From: AI Agents Book, Chapter 18, Section 18.2
# File: exercise_2_18_2_solution.py
# Description: Exercise 2 Solution - Sentiment routing with integration tests

import pytest
from unittest.mock import MagicMock, AsyncMock
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage


class SentimentState(TypedDict):
    messages: Annotated[list, add_messages]
    sentiment: str | None
    handler_invoked: str | None
    response: str | None


def classify_sentiment(state: SentimentState, llm) -> dict:
    """Classify the sentiment of the last message."""
    last_message = state["messages"][-1].content
    
    response = llm.invoke([HumanMessage(content=f"Classify sentiment: {last_message}")])
    sentiment = response.content.strip().lower()
    
    # Normalize to expected values
    if sentiment not in ["positive", "negative", "neutral"]:
        sentiment = "neutral"
    
    return {"sentiment": sentiment}


def route_by_sentiment(state: SentimentState) -> str:
    """Route to appropriate handler based on sentiment."""
    sentiment = state.get("sentiment", "neutral")
    
    if sentiment == "positive":
        return "handle_positive"
    elif sentiment == "negative":
        return "handle_negative"
    else:
        return "handle_neutral"


def handle_positive(state: SentimentState) -> dict:
    """Handle positive sentiment messages."""
    return {
        "handler_invoked": "positive",
        "response": "Thank you for your positive feedback! We're glad you're happy.",
        "messages": [AIMessage(content="Thank you for your positive feedback!")]
    }


def handle_negative(state: SentimentState) -> dict:
    """Handle negative sentiment messages."""
    return {
        "handler_invoked": "negative",
        "response": "We're sorry to hear you're unhappy. Let us help resolve this.",
        "messages": [AIMessage(content="We're sorry to hear that. How can we help?")]
    }


def handle_neutral(state: SentimentState) -> dict:
    """Handle neutral sentiment messages."""
    return {
        "handler_invoked": "neutral",
        "response": "Thank you for reaching out. How can we assist you today?",
        "messages": [AIMessage(content="How can we assist you today?")]
    }


def build_sentiment_graph(llm):
    """Build the sentiment routing graph."""
    graph = StateGraph(SentimentState)
    
    graph.add_node("classify_sentiment", lambda s: classify_sentiment(s, llm))
    graph.add_node("handle_positive", handle_positive)
    graph.add_node("handle_negative", handle_negative)
    graph.add_node("handle_neutral", handle_neutral)
    
    graph.add_edge(START, "classify_sentiment")
    graph.add_conditional_edges("classify_sentiment", route_by_sentiment)
    graph.add_edge("handle_positive", END)
    graph.add_edge("handle_negative", END)
    graph.add_edge("handle_neutral", END)
    
    return graph.compile()


# Integration tests
class TestSentimentRouting:
    """Integration tests for sentiment-based routing."""
    
    @pytest.fixture
    def mock_llm_positive(self):
        """Mock LLM that classifies as positive."""
        llm = MagicMock()
        llm.invoke.return_value = MagicMock(content="positive")
        return llm
    
    @pytest.fixture
    def mock_llm_negative(self):
        """Mock LLM that classifies as negative."""
        llm = MagicMock()
        llm.invoke.return_value = MagicMock(content="negative")
        return llm
    
    @pytest.fixture
    def mock_llm_neutral(self):
        """Mock LLM that classifies as neutral."""
        llm = MagicMock()
        llm.invoke.return_value = MagicMock(content="neutral")
        return llm
    
    def test_positive_sentiment_routes_to_positive_handler(self, mock_llm_positive):
        """Test that positive sentiment routes correctly."""
        graph = build_sentiment_graph(mock_llm_positive)
        
        initial_state = {
            "messages": [HumanMessage(content="I love your product!")],
            "sentiment": None,
            "handler_invoked": None,
            "response": None
        }
        
        result = graph.invoke(initial_state)
        
        assert result["sentiment"] == "positive"
        assert result["handler_invoked"] == "positive"
        assert "positive feedback" in result["response"].lower()
    
    def test_negative_sentiment_routes_to_negative_handler(self, mock_llm_negative):
        """Test that negative sentiment routes correctly."""
        graph = build_sentiment_graph(mock_llm_negative)
        
        initial_state = {
            "messages": [HumanMessage(content="This is terrible!")],
            "sentiment": None,
            "handler_invoked": None,
            "response": None
        }
        
        result = graph.invoke(initial_state)
        
        assert result["sentiment"] == "negative"
        assert result["handler_invoked"] == "negative"
        assert "sorry" in result["response"].lower()
    
    def test_neutral_sentiment_routes_to_neutral_handler(self, mock_llm_neutral):
        """Test that neutral sentiment routes correctly."""
        graph = build_sentiment_graph(mock_llm_neutral)
        
        initial_state = {
            "messages": [HumanMessage(content="What are your hours?")],
            "sentiment": None,
            "handler_invoked": None,
            "response": None
        }
        
        result = graph.invoke(initial_state)
        
        assert result["sentiment"] == "neutral"
        assert result["handler_invoked"] == "neutral"
        assert "assist" in result["response"].lower()
    
    def test_unknown_sentiment_defaults_to_neutral(self):
        """Test that unrecognized sentiment defaults to neutral."""
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content="confused")
        
        graph = build_sentiment_graph(mock_llm)
        
        initial_state = {
            "messages": [HumanMessage(content="...")],
            "sentiment": None,
            "handler_invoked": None,
            "response": None
        }
        
        result = graph.invoke(initial_state)
        
        # Should normalize to neutral
        assert result["sentiment"] == "neutral"
        assert result["handler_invoked"] == "neutral"
    
    def test_llm_is_called_with_user_message(self, mock_llm_positive):
        """Verify the LLM receives the user's message for classification."""
        graph = build_sentiment_graph(mock_llm_positive)
        
        test_message = "This is my specific test message"
        initial_state = {
            "messages": [HumanMessage(content=test_message)],
            "sentiment": None,
            "handler_invoked": None,
            "response": None
        }
        
        graph.invoke(initial_state)
        
        # Verify LLM was called
        mock_llm_positive.invoke.assert_called_once()
        
        # Verify the message content was passed
        call_args = mock_llm_positive.invoke.call_args[0][0]
        assert any(test_message in str(msg) for msg in call_args)
    
    def test_response_message_added_to_state(self, mock_llm_positive):
        """Verify handler adds response to messages."""
        graph = build_sentiment_graph(mock_llm_positive)
        
        initial_state = {
            "messages": [HumanMessage(content="Great service!")],
            "sentiment": None,
            "handler_invoked": None,
            "response": None
        }
        
        result = graph.invoke(initial_state)
        
        # Should have original message plus AI response
        assert len(result["messages"]) >= 2
        
        # Last message should be from AI
        ai_messages = [m for m in result["messages"] if isinstance(m, AIMessage)]
        assert len(ai_messages) >= 1
