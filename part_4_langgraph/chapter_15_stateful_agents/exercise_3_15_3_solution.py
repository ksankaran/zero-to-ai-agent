# From: Zero to AI Agent, Chapter 15, Section 15.3
# File: exercise_3_15_3_solution.py

"""
State that tracks all changes in a changelog.
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END
from datetime import datetime

class TrackedState(TypedDict):
    # Regular fields
    counter: int
    status: str
    # Changelog accumulates
    changelog: Annotated[list[dict], add]

def make_change_entry(node_name: str, changes: dict) -> dict:
    """Create a changelog entry."""
    return {
        "node": node_name,
        "time": datetime.now().strftime("%H:%M:%S"),
        "changes": changes
    }

def initialize(state):
    changes = {"counter": "0 → 1", "status": "→ initialized"}
    return {
        "counter": 1,
        "status": "initialized",
        "changelog": [make_change_entry("initialize", changes)]
    }

def process(state):
    new_counter = state["counter"] + 10
    changes = {"counter": f"{state['counter']} → {new_counter}"}
    return {
        "counter": new_counter,
        "changelog": [make_change_entry("process", changes)]
    }

def finalize(state):
    changes = {"status": f"{state['status']} → complete"}
    return {
        "status": "complete",
        "changelog": [make_change_entry("finalize", changes)]
    }

# Build graph
graph = StateGraph(TrackedState)
graph.add_node("init", initialize)
graph.add_node("proc", process)
graph.add_node("final", finalize)
graph.add_edge(START, "init")
graph.add_edge("init", "proc")
graph.add_edge("proc", "final")
graph.add_edge("final", END)

app = graph.compile()
result = app.invoke({"counter": 0, "status": "", "changelog": []})

print("=== Change Tracker ===")
print(f"\nFinal state: counter={result['counter']}, status={result['status']}")
print("\nChangelog:")
for entry in result['changelog']:
    print(f"  [{entry['time']}] {entry['node']}: {entry['changes']}")
