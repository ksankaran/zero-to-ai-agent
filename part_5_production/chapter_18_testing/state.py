# From: AI Agents Book, Chapter 18, Section 18.1
# File: state.py
# Description: Agent state definitions and helper functions for state transformations

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import add_messages


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    current_tool: str | None
    retry_count: int


def should_retry(state: AgentState, max_retries: int = 3) -> bool:
    """Determine if we should retry the current operation."""
    return state["retry_count"] < max_retries


def increment_retry(state: AgentState) -> dict:
    """Return state update to increment retry count."""
    return {"retry_count": state["retry_count"] + 1}


def reset_retry(state: AgentState) -> dict:
    """Return state update to reset retry count."""
    return {"retry_count": 0}
