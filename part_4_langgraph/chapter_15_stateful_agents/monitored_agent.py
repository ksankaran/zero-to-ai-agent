# From: Zero to AI Agent, Chapter 15, Section 15.7
# File: monitored_agent.py

"""
Example agent with monitoring.
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from datetime import datetime
import time

class AgentState(TypedDict):
    task: str
    steps: Annotated[list[str], add]
    result: str

# Simple metrics
metrics = {"nodes_run": 0, "total_time": 0.0}

def timed_node(name: str):
    """Decorator to add timing to nodes."""
    def decorator(func):
        def wrapper(state):
            start = time.time()
            result = func(state)
            elapsed = time.time() - start
            
            metrics["nodes_run"] += 1
            metrics["total_time"] += elapsed
            
            print(f"  ✓ {name} ({elapsed:.3f}s)")
            return result
        return wrapper
    return decorator

@timed_node("analyze")
def analyze(state: AgentState) -> dict:
    time.sleep(0.1)  # Simulate work
    return {"steps": [f"Analyzed: {state['task']}"]}

@timed_node("process")
def process(state: AgentState) -> dict:
    time.sleep(0.2)  # Simulate work
    return {"steps": ["Processed data"]}

@timed_node("complete")
def complete(state: AgentState) -> dict:
    time.sleep(0.05)  # Simulate work
    return {"result": "Done!", "steps": ["Completed"]}

# Build graph
graph = StateGraph(AgentState)
graph.add_node("analyze", analyze)
graph.add_node("process", process)
graph.add_node("complete", complete)
graph.add_edge(START, "analyze")
graph.add_edge("analyze", "process")
graph.add_edge("process", "complete")
graph.add_edge("complete", END)

app = graph.compile(checkpointer=MemorySaver())

# Run with monitoring
if __name__ == "__main__":
    print("🚀 Running monitored agent...\n")
    config = {"configurable": {"thread_id": "monitored-run"}}
    
    result = app.invoke({
        "task": "Process important data",
        "steps": [],
        "result": ""
    }, config)
    
    # Report
    print(f"\n📊 Metrics:")
    print(f"  Nodes run: {metrics['nodes_run']}")
    print(f"  Total time: {metrics['total_time']:.3f}s")
    print(f"\n✅ Result: {result['result']}")
    print(f"📝 Steps: {result['steps']}")
