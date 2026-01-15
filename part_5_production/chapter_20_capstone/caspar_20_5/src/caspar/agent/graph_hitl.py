# From: Zero to AI Agent, Chapter 20, Section 20.5
# File: src/caspar/agent/graph_hitl.py

"""
CASPAR Agent Graph with Human-in-the-Loop Interrupt Support

This module extends the base graph to add HITL approval for high-stakes responses.
"""

from langgraph.graph import StateGraph, END
from langgraph.types import interrupt, Command

from caspar.config import get_logger
from caspar.handoff.approval import needs_approval, get_approval_reason
from .state import AgentState
from .nodes import (
    classify_intent,
    handle_faq,
    handle_order_inquiry,
    handle_account,
    handle_complaint,
    handle_general,
    respond,
)
from .nodes_handoff_update import check_sentiment, human_handoff

logger = get_logger(__name__)


async def check_approval_needed(state: AgentState) -> dict:
    """
    Check if the pending response needs human approval.
    
    If approval is needed, we'll interrupt here and wait.
    """
    if not needs_approval(state):
        # No approval needed, continue normally
        return {"approval_status": "not_required"}
    
    # Get the pending response (generated but not yet sent)
    pending_response = state.get("pending_response", "")
    reason = get_approval_reason(state)
    
    logger.info(
        "approval_required",
        conversation_id=state.get("conversation_id"),
        reason=reason
    )
    
    # ════════════════════════════════════════════════════════════
    # THIS IS THE KEY: interrupt() pauses the graph!
    # ════════════════════════════════════════════════════════════
    # 
    # The graph stops here and returns control to the caller.
    # The caller must invoke the graph again with a Command to resume.
    #
    human_decision = interrupt({
        "type": "approval_required",
        "pending_response": pending_response,
        "reason": reason,
        "conversation_id": state.get("conversation_id"),
        "customer_id": state.get("customer_id"),
    })
    
    # When the graph resumes, human_decision contains:
    # {
    #     "approved": True/False,
    #     "edited_response": "..." (optional),
    #     "reviewer_id": "agent-123"
    # }
    
    if human_decision.get("approved"):
        # Use edited response if provided, otherwise use original
        final_response = human_decision.get("edited_response") or pending_response
        return {
            "approval_status": "approved",
            "pending_response": final_response,
            "reviewed_by": human_decision.get("reviewer_id"),
        }
    else:
        # Human rejected - don't send the response
        return {
            "approval_status": "rejected",
            "reviewed_by": human_decision.get("reviewer_id"),
            "needs_escalation": True,  # Human will handle directly
        }


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


def route_after_approval(state: AgentState) -> str:
    """Route after approval check."""
    status = state.get("approval_status", "not_required")
    if status == "not_required" or status == "approved":
        return "send_response"
    else:
        # Rejected - end the workflow, human will handle
        return END


async def send_response(state: AgentState) -> dict:
    """Send the final response to the customer."""
    # In a real system, this would send via the appropriate channel
    logger.info("send_response", conversation_id=state.get("conversation_id"))
    return {"response_sent": True}


def build_graph_with_approval() -> StateGraph:
    """
    Build the agent graph with human approval interrupt.
    
    The flow becomes:
    classify → handle_* → check_sentiment → respond 
        → check_approval → (INTERRUPT if needed) → send_response
    """
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
    graph.add_node("check_approval_needed", check_approval_needed)
    graph.add_node("send_response", send_response)
    
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
    
    # After respond, check if approval needed
    graph.add_edge("respond", "check_approval_needed")
    
    # After approval check, route based on status
    graph.add_conditional_edges(
        "check_approval_needed",
        route_after_approval,
        {
            "send_response": "send_response",
            END: END,
        }
    )
    
    # End nodes
    graph.add_edge("send_response", END)
    graph.add_edge("human_handoff", END)
    
    return graph


async def create_agent_with_approval(checkpointer=None):
    """
    Create agent with human approval support.
    
    IMPORTANT: A checkpointer is REQUIRED for interrupts to work!
    The graph state must be persisted so it can resume later.
    """
    graph = build_graph_with_approval()
    
    if checkpointer is None:
        raise ValueError(
            "Checkpointer is required for interrupt support. "
            "The graph must persist state to resume after approval."
        )
    
    # Compile with the checkpointer
    return graph.compile(checkpointer=checkpointer)


# Example: API endpoint handling interrupts
async def process_message_with_approval(
    agent,
    conversation_id: str, 
    message: str,
    state: dict,
) -> dict:
    """
    Process a message, handling potential interrupts.
    
    Returns either a response or an approval request.
    """
    from langchain_core.messages import HumanMessage
    
    state["messages"].append(HumanMessage(content=message))
    
    config = {"configurable": {"thread_id": conversation_id}}
    
    # Run the graph
    result = await agent.ainvoke(state, config)
    
    # Check if we hit an interrupt
    if hasattr(result, '__interrupt__'):
        # Graph is paused, waiting for approval
        interrupt_data = result.__interrupt__[0].value
        
        return {
            "status": "awaiting_approval",
            "pending_response": interrupt_data["pending_response"],
            "reason": interrupt_data["reason"],
            "conversation_id": conversation_id,
        }
    
    # Normal response
    return {
        "status": "complete",
        "response": result["messages"][-1].content,
    }


async def submit_approval(
    agent,
    conversation_id: str,
    approved: bool,
    edited_response: str | None = None,
    reviewer_id: str = None
) -> dict:
    """
    Submit human approval decision and resume the workflow.
    """
    config = {"configurable": {"thread_id": conversation_id}}
    
    # Resume the graph with the human's decision
    result = await agent.ainvoke(
        Command(resume={
            "approved": approved,
            "edited_response": edited_response,
            "reviewer_id": reviewer_id,
        }),
        config
    )
    
    if approved:
        return {
            "status": "complete",
            "response": result["messages"][-1].content,
        }
    else:
        return {
            "status": "escalated",
            "message": "Conversation transferred to human agent",
        }
