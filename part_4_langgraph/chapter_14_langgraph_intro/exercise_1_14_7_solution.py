# From: Building AI Agents, Chapter 14, Section 14.7
# File: exercise_1_14_7_solution.py

"""Ticket router with full debugging capabilities.

Exercise 1 Solution: Add comprehensive debugging to the ticket router:
- Debug output for every node
- State tracking
- Loop counter safety valve
- Graph visualization at startup
"""

import os
from typing import TypedDict
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Debug flag - set to False in production
DEBUG = True


def debug_print(*args, **kwargs):
    """Print only when DEBUG is True."""
    if DEBUG:
        print(*args, **kwargs)


# === STATE (with safety counter) ===

class TicketState(TypedDict):
    ticket_text: str
    category: str
    priority: str
    response: str
    needs_human: bool
    # Safety counter (even though this graph shouldn't loop)
    node_visits: int


# === STATE TRACKER ===

class StateTracker:
    """Track state changes throughout execution."""
    
    def __init__(self):
        self.history = []
    
    def capture(self, node_name: str, state: dict, updates: dict = None):
        import copy
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "node": node_name,
            "state": copy.deepcopy(dict(state)),
            "updates": copy.deepcopy(updates) if updates else None
        })
    
    def print_summary(self):
        print("\n" + "=" * 60)
        print("📜 EXECUTION TRACE")
        print("=" * 60)
        
        for i, entry in enumerate(self.history):
            print(f"\nStep {i+1}: {entry['node']}")
            if entry['updates']:
                for k, v in entry['updates'].items():
                    print(f"  → {k}: {str(v)[:50]}")


# Global tracker
tracker = StateTracker()


# === NODES (with debug output) ===

def classify_ticket(state: TicketState) -> dict:
    """Classify with full debug output."""
    debug_print(f"\n{'='*50}")
    debug_print(f"🔵 ENTERING: classify_ticket")
    debug_print(f"   Ticket: {state['ticket_text'][:40]}...")
    
    # Safety check
    visits = state.get("node_visits", 0) + 1
    if visits > 10:
        raise Exception("Safety limit: too many node visits!")
    
    ticket = state["ticket_text"]
    
    prompt = f"""Classify this support ticket.
    
    Ticket: {ticket}
    
    Categories: BILLING, TECHNICAL, ACCOUNT, GENERAL
    Priority: HIGH, MEDIUM, LOW
    
    Format:
    CATEGORY: <category>
    PRIORITY: <priority>"""
    
    response = llm.invoke(prompt)
    content = response.content.upper()
    
    # Parse with defaults
    category = "GENERAL"
    for cat in ["BILLING", "TECHNICAL", "ACCOUNT"]:
        if cat in content:
            category = cat
            break
    
    priority = "MEDIUM"
    for pri in ["HIGH", "LOW"]:
        if pri in content:
            priority = pri
            break
    
    updates = {
        "category": category,
        "priority": priority,
        "node_visits": visits
    }
    
    debug_print(f"   Result: {category} ({priority})")
    tracker.capture("classify_ticket", state, updates)
    
    return updates


def route_by_category(state: TicketState) -> str:
    """Route with debug output."""
    category = state["category"]
    priority = state["priority"]
    
    if priority == "HIGH":
        decision = "escalate"
    else:
        routes = {
            "BILLING": "handle_billing",
            "TECHNICAL": "handle_technical", 
            "ACCOUNT": "handle_account",
            "GENERAL": "handle_general"
        }
        decision = routes.get(category, "handle_general")
    
    debug_print(f"🔀 ROUTING: {decision}")
    debug_print(f"   (category={category}, priority={priority})")
    
    return decision


# === HANDLER FACTORY ===

def make_handler(name: str, emoji: str, specialty: str):
    """Factory to create debug-wrapped handlers."""
    
    def handler(state: TicketState) -> dict:
        debug_print(f"\n{'='*50}")
        debug_print(f"🔵 ENTERING: {name}")
        
        visits = state.get("node_visits", 0) + 1
        
        prompt = f"""You are a {specialty} specialist. Help with:
        {state['ticket_text']}
        Keep response brief (2-3 sentences)."""
        
        response = llm.invoke(prompt)
        
        updates = {
            "response": response.content,
            "needs_human": False,
            "node_visits": visits
        }
        
        debug_print(f"{emoji} Response generated")
        tracker.capture(name, state, updates)
        
        return updates
    
    return handler


# Create handlers
handle_billing = make_handler("handle_billing", "💳", "billing support")
handle_technical = make_handler("handle_technical", "🔧", "technical support")
handle_account = make_handler("handle_account", "👤", "account support")
handle_general = make_handler("handle_general", "📧", "general support")


def escalate_ticket(state: TicketState) -> dict:
    debug_print(f"\n{'='*50}")
    debug_print(f"🔵 ENTERING: escalate_ticket")
    
    updates = {
        "response": "Escalated to senior agent. Response within 1 hour.",
        "needs_human": True,
        "node_visits": state.get("node_visits", 0) + 1
    }
    
    debug_print("🚨 Ticket escalated!")
    tracker.capture("escalate_ticket", state, updates)
    
    return updates


# === GRAPH (with visualization) ===

def create_debug_router():
    """Build graph and show visualization."""
    graph = StateGraph(TicketState)
    
    graph.add_node("classify", classify_ticket)
    graph.add_node("handle_billing", handle_billing)
    graph.add_node("handle_technical", handle_technical)
    graph.add_node("handle_account", handle_account)
    graph.add_node("handle_general", handle_general)
    graph.add_node("escalate", escalate_ticket)
    
    graph.set_entry_point("classify")
    
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
    
    for handler in ["handle_billing", "handle_technical", 
                    "handle_account", "handle_general", "escalate"]:
        graph.add_edge(handler, END)
    
    app = graph.compile()
    
    # Show graph structure at startup
    if DEBUG:
        print("\n📊 GRAPH STRUCTURE")
        print("-" * 40)
        print(app.get_graph().draw_mermaid())
        print("-" * 40)
    
    return app


# === MAIN ===

def main():
    app = create_debug_router()
    
    test_tickets = [
        "I was charged twice!",
        "App keeps crashing",
        "THIS IS UNACCEPTABLE! FIX IT NOW!"
    ]
    
    for ticket in test_tickets:
        tracker.history.clear()  # Reset for each ticket
        
        print(f"\n{'='*60}")
        print(f"📩 Processing: {ticket}")
        print("=" * 60)
        
        result = app.invoke({
            "ticket_text": ticket,
            "category": "",
            "priority": "",
            "response": "",
            "needs_human": False,
            "node_visits": 0
        })
        
        # Print execution trace
        tracker.print_summary()
        
        print(f"\n✅ Final: {result['category']} → {result['response'][:50]}...")


if __name__ == "__main__":
    main()
