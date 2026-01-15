# From: Zero to AI Agent, Chapter 15, Section 15.3
# File: exercise_2_15_3_solution.py

"""
Reducer that maintains a priority-sorted task queue.
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END

def priority_queue(existing: list, new: list) -> list:
    """Merge tasks, keeping highest priority first."""
    combined = existing + new
    return sorted(combined, key=lambda x: x["priority"], reverse=True)

class TaskState(TypedDict):
    tasks: Annotated[list[dict], priority_queue]

def add_normal_tasks(state):
    return {"tasks": [
        {"task": "Write docs", "priority": 5},
        {"task": "Code review", "priority": 6}
    ]}

def add_urgent_task(state):
    return {"tasks": [
        {"task": "Fix critical bug", "priority": 10}
    ]}

def add_low_priority(state):
    return {"tasks": [
        {"task": "Update readme", "priority": 2}
    ]}

# Build graph
graph = StateGraph(TaskState)
graph.add_node("normal", add_normal_tasks)
graph.add_node("urgent", add_urgent_task)
graph.add_node("low", add_low_priority)
graph.add_edge(START, "normal")
graph.add_edge("normal", "urgent")
graph.add_edge("urgent", "low")
graph.add_edge("low", END)

app = graph.compile()
result = app.invoke({"tasks": []})

print("=== Priority Queue ===")
for task in result['tasks']:
    print(f"  [{task['priority']:2d}] {task['task']}")
