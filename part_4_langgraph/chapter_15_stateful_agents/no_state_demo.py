# From: Zero to AI Agent, Chapter 15, Section 15.1
# File: no_state_demo.py

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class CounterState(TypedDict):
    count: int

def increment(state: CounterState) -> dict:
    new_count = state["count"] + 1
    print(f"Count is now: {new_count}")
    return {"count": new_count}

graph = StateGraph(CounterState)
graph.add_node("increment", increment)
graph.add_edge(START, "increment")
graph.add_edge("increment", END)

app = graph.compile()  # No checkpointer!

# Run three times
for i in range(3):
    result = app.invoke({"count": 0})
