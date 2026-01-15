# From: AI Agents Book, Chapter 18, Section 18.1
# File: test_state.py
# Description: Unit tests for state transformation functions

from state import should_retry, increment_retry, reset_retry


def test_should_retry_under_limit():
    state = {"messages": [], "current_tool": None, "retry_count": 1}
    assert should_retry(state, max_retries=3) is True


def test_should_retry_at_limit():
    state = {"messages": [], "current_tool": None, "retry_count": 3}
    assert should_retry(state, max_retries=3) is False


def test_increment_retry():
    state = {"messages": [], "current_tool": None, "retry_count": 2}
    update = increment_retry(state)
    
    assert update == {"retry_count": 3}


def test_reset_retry():
    state = {"messages": [], "current_tool": None, "retry_count": 5}
    update = reset_retry(state)
    
    assert update == {"retry_count": 0}
