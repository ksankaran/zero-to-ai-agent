# From: Zero to AI Agent, Chapter 15, Section 15.2
# File: exercise_2_15_2_solution.py

"""
LangGraph node with Pydantic message validation.
"""

from typing import TypedDict, Annotated
from operator import add
from pydantic import BaseModel, Field, field_validator
from langgraph.graph import StateGraph, START, END

# Pydantic model for validation
class Message(BaseModel):
    role: str
    content: str
    
    @field_validator('role')
    @classmethod
    def valid_role(cls, v):
        if v not in ('user', 'assistant'):
            raise ValueError('Role must be "user" or "assistant"')
        return v
    
    @field_validator('content')
    @classmethod
    def content_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Content cannot be empty')
        return v.strip()

# TypedDict for LangGraph
class ChatState(TypedDict):
    messages: Annotated[list[dict], add]
    last_error: str

def validate_and_add_message(state: ChatState) -> dict:
    """Validate incoming message and add to state."""
    # Simulate incoming raw message
    raw_message = {"role": "user", "content": "  Hello there!  "}
    
    try:
        validated = Message(**raw_message)
        return {
            "messages": [validated.model_dump()],
            "last_error": ""
        }
    except Exception as e:
        return {
            "last_error": str(e)
        }

# Build and test
graph = StateGraph(ChatState)
graph.add_node("validate", validate_and_add_message)
graph.add_edge(START, "validate")
graph.add_edge("validate", END)
app = graph.compile()

result = app.invoke({"messages": [], "last_error": ""})
print("=== Message Validation ===")
print(f"Messages: {result['messages']}")
print(f"Notice: content was trimmed!")
