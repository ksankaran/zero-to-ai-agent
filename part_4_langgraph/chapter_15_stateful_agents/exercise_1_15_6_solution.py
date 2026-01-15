# From: Zero to AI Agent, Chapter 15, Section 15.6
# File: exercise_1_15_6_solution.py

"""
Multi-source aggregator with failure handling.
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END
import random

class AggregatorState(TypedDict):
    query: str
    results: Annotated[list[dict], add]
    errors: Annotated[list[str], add]

def make_source(name: str, fail_rate: float = 0.5):
    """Create a source node with configurable failure rate."""
    def source_node(state: AggregatorState) -> dict:
        if random.random() < fail_rate:
            return {"errors": [f"{name}: Connection failed"]}
        return {"results": [{"source": name, "data": f"Data from {name}"}]}
    return source_node

def aggregate(state: AggregatorState) -> dict:
    """Aggregate results and compute confidence."""
    successes = len(state["results"])
    failures = len(state["errors"])
    total = successes + failures
    
    confidence = successes / total if total > 0 else 0
    
    print(f"\n=== Aggregation Results ===")
    print(f"Succeeded: {successes}/{total}")
    print(f"Confidence: {confidence:.0%}")
    
    if state["results"]:
        print("\nData received:")
        for r in state["results"]:
            print(f"  ✓ {r['source']}: {r['data']}")
    
    if state["errors"]:
        print("\nFailures:")
        for e in state["errors"]:
            print(f"  ✗ {e}")
    
    return {}

# Build graph with 4 sources
graph = StateGraph(AggregatorState)

graph.add_node("source_a", make_source("Source A", 0.3))
graph.add_node("source_b", make_source("Source B", 0.7))
graph.add_node("source_c", make_source("Source C", 0.5))
graph.add_node("source_d", make_source("Source D", 0.4))
graph.add_node("aggregate", aggregate)

# All sources run, then aggregate
graph.add_edge(START, "source_a")
graph.add_edge(START, "source_b")
graph.add_edge(START, "source_c")
graph.add_edge(START, "source_d")
graph.add_edge("source_a", "aggregate")
graph.add_edge("source_b", "aggregate")
graph.add_edge("source_c", "aggregate")
graph.add_edge("source_d", "aggregate")
graph.add_edge("aggregate", END)

app = graph.compile()

# Run it
print("=== Multi-Source Aggregator Demo ===")
result = app.invoke({"query": "test", "results": [], "errors": []})
