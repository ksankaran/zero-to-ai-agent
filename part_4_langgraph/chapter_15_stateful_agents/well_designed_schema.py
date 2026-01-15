# From: Zero to AI Agent, Chapter 15, Section 15.2
# File: well_designed_schema.py

"""
Example of a well-designed state schema.
"""

from typing import TypedDict, Annotated, Optional
from operator import add
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

# Enums for controlled values
class AgentStatus(str, Enum):
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    DONE = "done"
    ERROR = "error"

# Pydantic for validated sub-structures
class Message(BaseModel):
    role: str = Field(pattern=r'^(user|assistant|system)$')
    content: str = Field(min_length=1)
    timestamp: datetime = Field(default_factory=datetime.now)

# TypedDict for LangGraph state
class AgentState(TypedDict):
    """
    Main state for the conversational agent.
    
    Fields marked with Annotated[..., add] accumulate across nodes.
    Other fields are replaced with new values.
    """
    # Accumulating fields
    messages: Annotated[list[dict], add]
    action_log: Annotated[list[str], add]
    
    # Replacing fields
    status: str  # Use AgentStatus values
    current_task: Optional[str]
    iteration: int

# Validation helper
def validate_message(msg: dict) -> dict:
    """Validate and normalize a message."""
    validated = Message(**msg)
    return validated.model_dump()
