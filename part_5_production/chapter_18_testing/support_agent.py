# From: AI Agents Book, Chapter 18, Section 18.2
# File: support_agent.py
# Description: Example support agent with classification and routing

from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage


class SupportState(TypedDict):
    messages: Annotated[list, add_messages]
    issue_type: str | None
    resolved: bool


def classify_issue(state: SupportState) -> dict:
    """Classify the customer's issue based on their message."""
    last_message = state["messages"][-1].content.lower()
    
    if "refund" in last_message or "money back" in last_message:
        return {"issue_type": "refund"}
    elif "broken" in last_message or "not working" in last_message:
        return {"issue_type": "technical"}
    elif "cancel" in last_message:
        return {"issue_type": "cancellation"}
    else:
        return {"issue_type": "general"}


def route_by_issue(state: SupportState) -> str:
    """Route to appropriate handler based on issue type."""
    issue_type = state.get("issue_type")
    if issue_type == "refund":
        return "handle_refund"
    elif issue_type == "technical":
        return "handle_technical"
    elif issue_type == "cancellation":
        return "handle_cancellation"
    else:
        return "handle_general"


def handle_refund(state: SupportState, llm) -> dict:
    """Handle refund requests."""
    response = llm.invoke(state["messages"] + [
        HumanMessage(content="Generate a helpful response about our refund policy.")
    ])
    return {
        "messages": [AIMessage(content=response.content)],
        "resolved": True
    }


def handle_technical(state: SupportState, llm) -> dict:
    """Handle technical issues."""
    response = llm.invoke(state["messages"] + [
        HumanMessage(content="Generate a helpful response for technical support.")
    ])
    return {
        "messages": [AIMessage(content=response.content)],
        "resolved": True
    }


def handle_cancellation(state: SupportState, llm) -> dict:
    """Handle cancellation requests."""
    response = llm.invoke(state["messages"] + [
        HumanMessage(content="Generate a helpful response about cancellation.")
    ])
    return {
        "messages": [AIMessage(content=response.content)],
        "resolved": True
    }


def handle_general(state: SupportState, llm) -> dict:
    """Handle general inquiries."""
    response = llm.invoke(state["messages"] + [
        HumanMessage(content="Generate a helpful general response.")
    ])
    return {
        "messages": [AIMessage(content=response.content)],
        "resolved": True
    }


def build_support_graph(llm):
    """Build the support agent graph."""
    graph = StateGraph(SupportState)
    
    graph.add_node("classify", classify_issue)
    graph.add_node("handle_refund", lambda s: handle_refund(s, llm))
    graph.add_node("handle_technical", lambda s: handle_technical(s, llm))
    graph.add_node("handle_cancellation", lambda s: handle_cancellation(s, llm))
    graph.add_node("handle_general", lambda s: handle_general(s, llm))
    
    graph.add_edge(START, "classify")
    graph.add_conditional_edges("classify", route_by_issue)
    graph.add_edge("handle_refund", END)
    graph.add_edge("handle_technical", END)
    graph.add_edge("handle_cancellation", END)
    graph.add_edge("handle_general", END)
    
    return graph.compile()
