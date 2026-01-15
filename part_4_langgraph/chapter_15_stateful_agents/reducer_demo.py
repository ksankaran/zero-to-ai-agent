# From: Zero to AI Agent, Chapter 15, Section 15.3
# File: reducer_demo.py

"""
Demonstrates the difference between accumulating and replacing state fields.
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    items: Annotated[list[str], add]  # Will accumulate
    count: int                         # Will replace

def node_a(state):
    return {"items": ["from A"], "count": 1}

def node_b(state):
    return {"items": ["from B"], "count": 2}

graph = StateGraph(State)
graph.add_node("a", node_a)
graph.add_node("b", node_b)
graph.add_edge(START, "a")
graph.add_edge("a", "b")
graph.add_edge("b", END)

app = graph.compile()
result = app.invoke({"items": [], "count": 0})

print(f"items: {result['items']}")  # ['from A', 'from B'] - accumulated!
print(f"count: {result['count']}")  # 2 - replaced!
