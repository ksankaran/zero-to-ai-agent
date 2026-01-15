# From: Zero to AI Agent, Chapter 15, Section 15.1
# File: exercise_1_15_1_solution.py

"""
Agent that counts user visits and greets accordingly.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class VisitState(TypedDict):
    visit_count: int
    greeting: str

def greet_user(state: VisitState) -> dict:
    """Generate appropriate greeting based on visit count."""
    count = state["visit_count"] + 1
    
    if count == 1:
        greeting = "Welcome! This is your first visit."
    elif count == 2:
        greeting = "Welcome back! Good to see you again."
    else:
        greeting = f"Hello again! This is visit #{count}."
    
    return {"visit_count": count, "greeting": greeting}

# Build graph
graph = StateGraph(VisitState)
graph.add_node("greet", greet_user)
graph.add_edge(START, "greet")
graph.add_edge("greet", END)

app = graph.compile(checkpointer=MemorySaver())

# Simulate multiple visits
config = {"configurable": {"thread_id": "user-123"}}

print("=== Conversation Counter ===\n")
for i in range(4):
    result = app.invoke({"visit_count": 0, "greeting": ""}, config)
    print(f"Visit {i+1}: {result['greeting']}")
