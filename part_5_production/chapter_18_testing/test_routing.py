# From: AI Agents Book, Chapter 18, Section 18.1
# File: test_routing.py
# Description: Unit tests for conditional edge routing decisions

from unittest.mock import MagicMock
from routing import route_after_llm


def test_route_to_tools_when_tool_calls_present():
    mock_message = MagicMock()
    mock_message.tool_calls = [{"name": "search", "args": {"query": "test"}}]
    
    state = {"messages": [mock_message]}
    
    assert route_after_llm(state) == "execute_tools"


def test_route_to_goodbye_when_should_end():
    mock_message = MagicMock()
    mock_message.tool_calls = None
    
    state = {"messages": [mock_message], "should_end": True}
    
    assert route_after_llm(state) == "goodbye"


def test_route_to_respond_by_default():
    mock_message = MagicMock()
    mock_message.tool_calls = None
    
    state = {"messages": [mock_message], "should_end": False}
    
    assert route_after_llm(state) == "respond_to_user"


def test_route_to_error_when_no_messages():
    state = {"messages": []}
    
    assert route_after_llm(state) == "error_handler"
