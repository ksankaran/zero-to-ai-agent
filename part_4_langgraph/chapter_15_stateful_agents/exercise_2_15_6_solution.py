# From: Zero to AI Agent, Chapter 15, Section 15.6
# File: exercise_2_15_6_solution.py

"""
Fallback chain with source tracking.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import random

class FallbackState(TypedDict):
    query: str
    data: str
    source_used: str
    attempts: list[str]

def try_primary(state: FallbackState) -> dict:
    """Primary API - fails 70% of the time."""
    attempts = state.get("attempts", []) + ["primary"]
    
    if random.random() > 0.7:  # 30% success
        return {
            "data": "Fresh data from primary API",
            "source_used": "primary",
            "attempts": attempts
        }
    return {"attempts": attempts}

def try_secondary(state: FallbackState) -> dict:
    """Secondary API - fails 40% of the time."""
    if state.get("data"):  # Already have data
        return {}
    
    attempts = state.get("attempts", []) + ["secondary"]
    
    if random.random() > 0.4:  # 60% success
        return {
            "data": "Data from secondary API",
            "source_used": "secondary",
            "attempts": attempts
        }
    return {"attempts": attempts}

def try_cache(state: FallbackState) -> dict:
    """Cache - always succeeds but stale."""
    if state.get("data"):  # Already have data
        return {}
    
    attempts = state.get("attempts", []) + ["cache"]
    return {
        "data": "Stale data from cache (24h old)",
        "source_used": "cache",
        "attempts": attempts
    }

# Build graph
graph = StateGraph(FallbackState)
graph.add_node("primary", try_primary)
graph.add_node("secondary", try_secondary)
graph.add_node("cache", try_cache)

graph.add_edge(START, "primary")
graph.add_edge("primary", "secondary")
graph.add_edge("secondary", "cache")
graph.add_edge("cache", END)

app = graph.compile()

# Test multiple times
print("=== Fallback Chain Demo ===\n")

for i in range(5):
    result = app.invoke({
        "query": "test",
        "data": "",
        "source_used": "",
        "attempts": []
    })
    
    print(f"Run {i+1}:")
    print(f"  Source: {result['source_used']}")
    print(f"  Attempts: {' → '.join(result['attempts'])}")
    print(f"  Data: {result['data'][:30]}...")
    print()
