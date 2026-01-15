# From: Building AI Agents, Chapter 14, Section 14.6
# File: ticket_router.py

"""A support ticket router with multi-way branching.

Demonstrates Pattern 1: Multi-Way Branching
- Classification node analyzes ticket
- Routing function decides destination (5 options)
- Specialized handlers for each category
"""

import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


# === STATE ===

class TicketState(TypedDict):
    ticket_text: str          # The customer's message
    category: str             # Classified category (BILLING, TECHNICAL, etc.)
    priority: str             # Urgency level (HIGH, MEDIUM, LOW)
    response: str             # Generated response
    needs_human: bool         # Flag for escalation


# === CLASSIFICATION NODE ===

def classify_ticket(state: TicketState) -> dict:
    """Classify the ticket into a category and priority level.
    
    This node uses the LLM to analyze the ticket text and determine:
    1. What type of issue it is (billing, technical, account, general)
    2. How urgent it is (high, medium, low)
    
    High priority tickets will be escalated regardless of category.
    """
    ticket = state["ticket_text"]
    
    prompt = f"""Classify this support ticket into exactly one category.
    
    Ticket: {ticket}
    
    Categories:
    - BILLING: Payment issues, invoices, refunds, subscriptions
    - TECHNICAL: Bugs, errors, how-to questions, feature requests
    - ACCOUNT: Login issues, password reset, profile changes
    - GENERAL: Everything else
    
    Also determine priority:
    - HIGH: Customer is angry, service is down, money involved
    - MEDIUM: Normal requests, minor issues
    - LOW: Questions, feedback, suggestions
    
    Respond in format:
    CATEGORY: <category>
    PRIORITY: <priority>"""
    
    response = llm.invoke(prompt)
    content = response.content.upper()
    
    # Parse category from response - default to GENERAL if not found
    category = "GENERAL"
    for cat in ["BILLING", "TECHNICAL", "ACCOUNT"]:
        if cat in content:
            category = cat
            break
    
    # Parse priority from response - default to MEDIUM if not found
    priority = "MEDIUM"
    for pri in ["HIGH", "LOW"]:
        if pri in content:
            priority = pri
            break
    
    print(f"📋 Classified: {category} ({priority} priority)")
    
    return {
        "category": category,
        "priority": priority
    }


# === ROUTING FUNCTION ===

def route_by_category(state: TicketState) -> str:
    """Decide which handler should process this ticket.
    
    The routing logic:
    1. HIGH priority tickets always go to escalation (human needed)
    2. Otherwise, route to the specialized handler for that category
    
    Returns a string that matches one of our handler node names.
    """
    category = state["category"]
    priority = state["priority"]
    
    # High priority always escalates, regardless of category
    if priority == "HIGH":
        return "escalate"
    
    # Map categories to handler names
    routes = {
        "BILLING": "handle_billing",
        "TECHNICAL": "handle_technical",
        "ACCOUNT": "handle_account",
        "GENERAL": "handle_general"
    }
    
    return routes.get(category, "handle_general")


# === HANDLER NODES ===

def handle_billing(state: TicketState) -> dict:
    """Handle billing-related tickets.
    
    Specializes in: payments, invoices, refunds, subscription issues.
    Uses a billing-focused prompt that knows about refund policies.
    """
    ticket = state["ticket_text"]
    
    prompt = f"""You are a billing support specialist. Help with this issue:
    
    {ticket}
    
    Be helpful and mention our refund policy if relevant.
    Keep response concise (2-3 sentences)."""
    
    response = llm.invoke(prompt)
    print("💳 Billing handler responded")
    
    return {"response": response.content, "needs_human": False}


def handle_technical(state: TicketState) -> dict:
    """Handle technical support tickets.
    
    Specializes in: bugs, errors, how-to questions, troubleshooting.
    Provides clear, step-by-step guidance.
    """
    ticket = state["ticket_text"]
    
    prompt = f"""You are a technical support specialist. Help with this issue:
    
    {ticket}
    
    Provide clear troubleshooting steps.
    Keep response concise (2-3 sentences)."""
    
    response = llm.invoke(prompt)
    print("🔧 Technical handler responded")
    
    return {"response": response.content, "needs_human": False}


def handle_account(state: TicketState) -> dict:
    """Handle account-related tickets.
    
    Specializes in: login issues, password reset, profile changes.
    Prioritizes security in responses.
    """
    ticket = state["ticket_text"]
    
    prompt = f"""You are an account support specialist. Help with this issue:
    
    {ticket}
    
    Prioritize security and verification.
    Keep response concise (2-3 sentences)."""
    
    response = llm.invoke(prompt)
    print("👤 Account handler responded")
    
    return {"response": response.content, "needs_human": False}


def handle_general(state: TicketState) -> dict:
    """Handle general inquiries that don't fit other categories."""
    ticket = state["ticket_text"]
    
    prompt = f"""You are a friendly support agent. Help with this inquiry:
    
    {ticket}
    
    Be warm and helpful.
    Keep response concise (2-3 sentences)."""
    
    response = llm.invoke(prompt)
    print("📧 General handler responded")
    
    return {"response": response.content, "needs_human": False}


def escalate_ticket(state: TicketState) -> dict:
    """Escalate high-priority tickets to human agents.
    
    This node doesn't try to solve the problem—it acknowledges
    the urgency and promises human follow-up.
    """
    print("🚨 Escalating to human agent")
    
    return {
        "response": "This ticket has been escalated to a senior support agent who will contact you within 1 hour.",
        "needs_human": True
    }


# === GRAPH BUILDER ===

def create_router_graph():
    """Build the ticket routing graph.
    
    The flow:
    1. classify - Analyze the ticket
    2. route_by_category - Decide which handler (conditional edge)
    3. One of five handlers runs
    4. END
    """
    graph = StateGraph(TicketState)
    
    # Add all our nodes
    graph.add_node("classify", classify_ticket)
    graph.add_node("handle_billing", handle_billing)
    graph.add_node("handle_technical", handle_technical)
    graph.add_node("handle_account", handle_account)
    graph.add_node("handle_general", handle_general)
    graph.add_node("escalate", escalate_ticket)
    
    # Start at classification
    graph.set_entry_point("classify")
    
    # After classification, route to the appropriate handler
    # This is the key part - 5-way conditional branching!
    graph.add_conditional_edges(
        "classify",
        route_by_category,
        {
            "handle_billing": "handle_billing",
            "handle_technical": "handle_technical",
            "handle_account": "handle_account",
            "handle_general": "handle_general",
            "escalate": "escalate"
        }
    )
    
    # All handlers lead to END (no loops in this graph)
    graph.add_edge("handle_billing", END)
    graph.add_edge("handle_technical", END)
    graph.add_edge("handle_account", END)
    graph.add_edge("handle_general", END)
    graph.add_edge("escalate", END)
    
    return graph.compile()


# === MAIN ===

def main():
    """Test the ticket router with different types of tickets."""
    app = create_router_graph()
    
    test_tickets = [
        "I was charged twice for my subscription last month!",
        "How do I reset my password?",
        "The app crashes whenever I try to upload a photo",
        "What are your business hours?",
        "THIS IS OUTRAGEOUS! Your service has been down for 3 hours!"
    ]
    
    print("=" * 60)
    print("🎫 Support Ticket Router")
    print("=" * 60)
    
    for ticket in test_tickets:
        print(f"\n📩 Ticket: {ticket[:50]}...")
        print("-" * 40)
        
        result = app.invoke({
            "ticket_text": ticket,
            "category": "",
            "priority": "",
            "response": "",
            "needs_human": False
        })
        
        print(f"📤 Response: {result['response'][:100]}...")
        if result["needs_human"]:
            print("⚠️  Escalated to human")


if __name__ == "__main__":
    main()
