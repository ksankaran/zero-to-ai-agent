# From: Zero to AI Agent, Chapter 20, Section 20.2
# File: src/caspar/agent/graph.py

"""
CASPAR Agent Graph

This module defines the LangGraph workflow that orchestrates
the customer service agent. The graph connects nodes with
conditional edges to create intelligent conversation routing.
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from caspar.config import settings, get_logger
from .state import AgentState
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

logger = get_logger(__name__)


def route_by_intent(state: AgentState) -> str:
    """
    Route to the appropriate handler based on classified intent.
    
    This function is used as a conditional edge to direct flow
    after intent classification.
    
    Args:
        state: Current agent state with 'intent' field populated
        
    Returns:
        Name of the next node to execute
    """
    intent = state.get("intent", "general")
    
    # Immediate handoff if requested
    if intent == "handoff_request":
        return "human_handoff"
    
    # Route to appropriate handler
    intent_to_handler = {
        "faq": "handle_faq",
        "order_inquiry": "handle_order_inquiry",
        "complaint": "handle_complaint",
        "general": "handle_general",
    }
    
    return intent_to_handler.get(intent, "handle_general")


def route_after_sentiment(state: AgentState) -> str:
    """
    Route based on sentiment check results.
    
    After checking sentiment, we either respond normally
    or escalate to human handoff if frustration is high.
    
    Args:
        state: Current state with sentiment analysis results
        
    Returns:
        Either 'respond' or 'human_handoff'
    """
    if state.get("needs_escalation", False):
        return "human_handoff"
    return "respond"


def build_graph() -> StateGraph:
    """
    Build the CASPAR agent graph.
    
    This creates the complete workflow with all nodes and edges.
    The graph is not yet compiled - call compile() on the result
    to get an executable graph.
    
    Returns:
        Configured StateGraph ready for compilation
    """
    logger.info("building_agent_graph")
    
    # Create the graph with our state schema
    graph = StateGraph(AgentState)
    
    # Add all nodes
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("handle_faq", handle_faq)
    graph.add_node("handle_order_inquiry", handle_order_inquiry)
    graph.add_node("handle_complaint", handle_complaint)
    graph.add_node("handle_general", handle_general)
    graph.add_node("check_sentiment", check_sentiment)
    graph.add_node("respond", respond)
    graph.add_node("human_handoff", human_handoff)
    
    # Define the flow
    
    # Start -> classify intent
    graph.add_edge(START, "classify_intent")
    
    # Intent classification -> route to appropriate handler
    graph.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "handle_faq": "handle_faq",
            "handle_order_inquiry": "handle_order_inquiry",
            "handle_complaint": "handle_complaint",
            "handle_general": "handle_general",
            "human_handoff": "human_handoff",
        }
    )
    
    # All handlers -> sentiment check
    graph.add_edge("handle_faq", "check_sentiment")
    graph.add_edge("handle_order_inquiry", "check_sentiment")
    graph.add_edge("handle_complaint", "check_sentiment")
    graph.add_edge("handle_general", "check_sentiment")
    
    # Sentiment check -> respond or escalate
    graph.add_conditional_edges(
        "check_sentiment",
        route_after_sentiment,
        {
            "respond": "respond",
            "human_handoff": "human_handoff",
        }
    )
    
    # Terminal nodes -> END
    graph.add_edge("respond", END)
    graph.add_edge("human_handoff", END)
    
    logger.info("agent_graph_built")
    
    return graph


async def create_agent(checkpointer: AsyncPostgresSaver | None = None):
    """
    Create a compiled, executable agent.
    
    Args:
        checkpointer: Optional PostgreSQL checkpointer for state persistence.
                     If provided, conversations can be resumed across sessions.
    
    Returns:
        Compiled LangGraph agent ready to process messages
    """
    graph = build_graph()
    
    if checkpointer:
        compiled = graph.compile(checkpointer=checkpointer)
        logger.info("agent_compiled_with_persistence")
    else:
        compiled = graph.compile()
        logger.info("agent_compiled_without_persistence")
    
    return compiled


# Export a simple way to visualize the graph (useful for debugging)
def get_graph_diagram() -> str:
    """
    Get a Mermaid diagram of the agent graph.
    
    Useful for documentation and debugging. You can render this
    at https://mermaid.live or in documentation tools.
    
    Returns:
        Mermaid diagram string
    """
    return """
graph TD
    START((Start)) --> classify_intent
    
    classify_intent --> |faq| handle_faq
    classify_intent --> |order_inquiry| handle_order_inquiry
    classify_intent --> |complaint| handle_complaint
    classify_intent --> |general| handle_general
    classify_intent --> |handoff_request| human_handoff
    
    handle_faq --> check_sentiment
    handle_order_inquiry --> check_sentiment
    handle_complaint --> check_sentiment
    handle_general --> check_sentiment
    
    check_sentiment --> |normal| respond
    check_sentiment --> |escalate| human_handoff
    
    respond --> END((End))
    human_handoff --> END
"""
