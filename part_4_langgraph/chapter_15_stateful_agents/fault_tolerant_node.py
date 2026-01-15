# From: Zero to AI Agent, Chapter 15, Section 15.6
# File: fault_tolerant_node.py

"""
Pattern for fault-tolerant nodes.
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END
import random

class RobustState(TypedDict):
    input: str
    results: Annotated[list[dict], add]
    warnings: Annotated[list[str], add]

def fault_tolerant_operation(
    name: str,
    operation: callable,
    fallback_value: any = None
):
    """
    Wrap an operation with fault tolerance.
    
    Returns a node function that:
    - Tries the operation
    - Falls back on failure
    - Always returns useful state
    """
    def node(state: RobustState) -> dict:
        try:
            result = operation(state)
            return {
                "results": [{"source": name, "data": result, "status": "ok"}]
            }
        except Exception as e:
            return {
                "results": [{"source": name, "data": fallback_value, "status": "failed"}],
                "warnings": [f"{name}: {str(e)}"]
            }
    return node

# Example operations (some will fail randomly)
def flaky_api(state):
    if random.random() < 0.5:
        raise ConnectionError("Service unavailable")
    return f"API data for {state['input']}"

def reliable_cache(state):
    return f"Cached data for {state['input']}"

def sometimes_slow(state):
    if random.random() < 0.3:
        raise TimeoutError("Request timed out")
    return f"Fresh data for {state['input']}"

# Build graph with fault-tolerant nodes
graph = StateGraph(RobustState)

graph.add_node("api", fault_tolerant_operation("API", flaky_api, "N/A"))
graph.add_node("cache", fault_tolerant_operation("Cache", reliable_cache, "N/A"))
graph.add_node("fresh", fault_tolerant_operation("Fresh", sometimes_slow, "N/A"))

graph.add_edge(START, "api")
graph.add_edge("api", "cache")
graph.add_edge("cache", "fresh")
graph.add_edge("fresh", END)

app = graph.compile()

# Test it multiple times
print("=== Fault Tolerant Node Demo ===\n")

for i in range(3):
    print(f"Run {i + 1}:")
    result = app.invoke({"input": "test query", "results": [], "warnings": []})
    
    for r in result["results"]:
        status = "✓" if r["status"] == "ok" else "✗"
        print(f"  {status} {r['source']}: {r['data']}")
    
    if result["warnings"]:
        print("  Warnings:")
        for w in result["warnings"]:
            print(f"    ⚠️ {w}")
    print()
