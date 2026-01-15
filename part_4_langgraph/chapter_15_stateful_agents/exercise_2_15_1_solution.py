# From: Zero to AI Agent, Chapter 15, Section 15.1
# File: exercise_2_15_1_solution.py

"""
Multi-user agent with separate state per user.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class UserState(TypedDict):
    user_name: str
    visit_count: int

def track_visit(state: UserState) -> dict:
    return {"visit_count": state["visit_count"] + 1}

# Build graph
graph = StateGraph(UserState)
graph.add_node("track", track_visit)
graph.add_edge(START, "track")
graph.add_edge("track", END)

app = graph.compile(checkpointer=MemorySaver())

def visit(user_name: str) -> int:
    """Simulate a user visit, return their visit count."""
    config = {"configurable": {"thread_id": f"user-{user_name}"}}
    result = app.invoke({"user_name": user_name, "visit_count": 0}, config)
    return result["visit_count"]

# Simulate visits from different users
print("=== Multi-User Tracker ===\n")

# Alice visits 3 times
for i in range(3):
    count = visit("alice")
    print(f"Alice visit: count = {count}")

print()

# Bob visits 2 times
for i in range(2):
    count = visit("bob")
    print(f"Bob visit: count = {count}")

print()

# Alice visits again - should continue from 3
count = visit("alice")
print(f"Alice visit: count = {count} (continued from before!)")
