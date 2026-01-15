# From: Zero to AI Agent, Chapter 20, Section 20.4
# File: src/caspar/agent/graph.py

"""CASPAR Agent Graph - defines the LangGraph workflow."""

from langgraph.graph import StateGraph, END

from caspar.config import get_logger
from .state import AgentState
from .nodes import (
    classify_intent,
    handle_faq,
    handle_order_inquiry,
    handle_account,
    handle_complaint,
    handle_general,
    check_sentiment,
    respond,
    human_handoff,
)

logger = get_logger(__name__)


def route_by_intent(state: AgentState) -> str:
    """Route to the appropriate handler based on classified intent."""
    intent = state.get("intent", "general")
    
    routes = {
        "faq": "handle_faq",
        "order_inquiry": "handle_order_inquiry",
        "account": "handle_account",
        "complaint": "handle_complaint",
        "handoff_request": "human_handoff",
        "general": "handle_general",
    }
    
    return routes.get(intent, "handle_general")


def route_after_sentiment(state: AgentState) -> str:
    """Route based on sentiment - escalate if needed."""
    if state.get("needs_escalation") and state.get("intent") != "handoff_request":
        return "human_handoff"
    return "respond"


def build_graph() -> StateGraph:
    """Build the CASPAR agent graph."""
    
    graph = StateGraph(AgentState)
    
    # Add all nodes
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("handle_faq", handle_faq)
    graph.add_node("handle_order_inquiry", handle_order_inquiry)
    graph.add_node("handle_account", handle_account)
    graph.add_node("handle_complaint", handle_complaint)
    graph.add_node("handle_general", handle_general)
    graph.add_node("check_sentiment", check_sentiment)
    graph.add_node("respond", respond)
    graph.add_node("human_handoff", human_handoff)
    
    # Set entry point
    graph.set_entry_point("classify_intent")
    
    # Route by intent
    graph.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "handle_faq": "handle_faq",
            "handle_order_inquiry": "handle_order_inquiry",
            "handle_account": "handle_account",
            "handle_complaint": "handle_complaint",
            "handle_general": "handle_general",
            "human_handoff": "human_handoff",
        }
    )
    
    # All handlers go to sentiment check
    for handler in ["handle_faq", "handle_order_inquiry", "handle_account", 
                    "handle_complaint", "handle_general"]:
        graph.add_edge(handler, "check_sentiment")
    
    # Sentiment routes to respond or escalate
    graph.add_conditional_edges(
        "check_sentiment",
        route_after_sentiment,
        {"respond": "respond", "human_handoff": "human_handoff"}
    )
    
    # End nodes
    graph.add_edge("respond", END)
    graph.add_edge("human_handoff", END)
    
    return graph


async def create_agent(checkpointer=None):
    """Create and compile the CASPAR agent."""
    graph = build_graph()
    return graph.compile(checkpointer=checkpointer) if checkpointer else graph.compile()


def get_graph_diagram() -> str:
    """Get a Mermaid diagram of the graph."""
    graph = build_graph()
    return graph.get_graph().draw_mermaid()
