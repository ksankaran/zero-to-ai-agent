# From: AI Agents Book, Chapter 18, Section 18.1
# File: test_nodes.py
# Description: Unit tests for node functions - demonstrates mocking LLM responses

import pytest
from unittest.mock import AsyncMock, MagicMock
from nodes import analyze_sentiment


@pytest.mark.asyncio
async def test_analyze_sentiment_positive():
    # Create mock LLM
    mock_llm = AsyncMock()
    mock_response = MagicMock()
    mock_response.content = "positive"
    mock_llm.ainvoke.return_value = mock_response
    
    # Create test state
    mock_message = MagicMock()
    mock_message.type = "human"
    mock_message.content = "I love this product!"
    state = {"messages": [mock_message]}
    
    result = await analyze_sentiment(state, mock_llm)
    
    assert result["sentiment"] == "positive"
    assert result["confidence"] == 0.85


@pytest.mark.asyncio
async def test_analyze_sentiment_handles_invalid_response():
    mock_llm = AsyncMock()
    mock_response = MagicMock()
    mock_response.content = "I think it's somewhat positive but also..."  # Invalid
    mock_llm.ainvoke.return_value = mock_response
    
    mock_message = MagicMock()
    mock_message.type = "human"
    mock_message.content = "It's okay I guess"
    state = {"messages": [mock_message]}
    
    result = await analyze_sentiment(state, mock_llm)
    
    assert result["sentiment"] == "unknown"  # Falls back gracefully


@pytest.mark.asyncio
async def test_analyze_sentiment_no_user_message():
    mock_llm = AsyncMock()
    
    state = {"messages": []}  # No messages
    
    result = await analyze_sentiment(state, mock_llm)
    
    assert result["sentiment"] == "unknown"
    assert result["confidence"] == 0.0
    mock_llm.ainvoke.assert_not_called()  # LLM shouldn't be called
