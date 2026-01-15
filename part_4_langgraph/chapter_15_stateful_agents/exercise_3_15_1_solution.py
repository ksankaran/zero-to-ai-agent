# From: Zero to AI Agent, Chapter 15, Section 15.1
# File: exercise_3_15_1_solution.py

"""
Explore state history through a multi-node workflow.
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class WorkflowState(TypedDict):
    steps_completed: Annotated[list[str], add]
    current_value: int

def step_one(state: WorkflowState) -> dict:
    return {
        "steps_completed": ["step_one"],
        "current_value": 10
    }

def step_two(state: WorkflowState) -> dict:
    return {
        "steps_completed": ["step_two"],
        "current_value": state["current_value"] * 2
    }

def step_three(state: WorkflowState) -> dict:
    return {
        "steps_completed": ["step_three"],
        "current_value": state["current_value"] + 5
    }

# Build graph
graph = StateGraph(WorkflowState)
graph.add_node("one", step_one)
graph.add_node("two", step_two)
graph.add_node("three", step_three)
graph.add_edge(START, "one")
graph.add_edge("one", "two")
graph.add_edge("two", "three")
graph.add_edge("three", END)

app = graph.compile(checkpointer=MemorySaver())

# Run the workflow
config = {"configurable": {"thread_id": "workflow-1"}}
result = app.invoke({"steps_completed": [], "current_value": 0}, config)

# Explore the history
print("=== State History Explorer ===\n")
print("Final result:", result)
print("\n--- History (newest first) ---\n")

for i, snapshot in enumerate(app.get_state_history(config)):
    print(f"Snapshot {i}:")
    print(f"  Steps: {snapshot.values.get('steps_completed', [])}")
    print(f"  Value: {snapshot.values.get('current_value', 'N/A')}")
    print(f"  Next: {snapshot.next}")
    print()
