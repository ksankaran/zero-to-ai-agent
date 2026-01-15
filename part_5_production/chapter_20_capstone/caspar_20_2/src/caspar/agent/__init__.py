# From: Zero to AI Agent, Chapter 20, Section 20.2
# File: src/caspar/agent/__init__.py

"""
CASPAR Agent Module

This module exposes the main agent interface for use by the API layer
and other components.
"""

from .state import AgentState, create_initial_state, ConversationMetadata
from .graph import build_graph, create_agent, get_graph_diagram
from .persistence import create_checkpointer_context
from .nodes import (
    classify_intent,
    handle_faq,
    handle_order_inquiry,
    handle_complaint,
    handle_general,
    check_sentiment,
    respond,
    human_handoff,
)

__all__ = [
    # State
    "AgentState",
    "create_initial_state",
    "ConversationMetadata",
    
    # Graph
    "build_graph",
    "create_agent",
    "get_graph_diagram",
    
    # Persistence
    "create_checkpointer_context",
    
    # Nodes (exported for testing)
    "classify_intent",
    "handle_faq",
    "handle_order_inquiry",
    "handle_complaint",
    "handle_general",
    "check_sentiment",
    "respond",
    "human_handoff",
]
