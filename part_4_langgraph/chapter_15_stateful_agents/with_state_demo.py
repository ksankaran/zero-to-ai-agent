# From: Zero to AI Agent, Chapter 15, Section 15.1
# File: with_state_demo.py

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

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

# Add checkpointer!
checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

# The secret ingredient: thread_id
config = {"configurable": {"thread_id": "my-counter"}}

# Run three times with SAME thread_id
for i in range(3):
    result = app.invoke({"count": 0}, config)
