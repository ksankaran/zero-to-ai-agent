# From: Zero to AI Agent, Chapter 15, Section 15.6
# File: graceful_degradation.py

"""
Graceful degradation pattern - continue with partial results when some sources fail.
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

class ResearchState(TypedDict):
    query: str
    results: Annotated[list[str], add]
    errors: Annotated[list[str], add]
    success_count: Annotated[int, add]  # Reducer needed for parallel updates
    failure_count: Annotated[int, add]  # Reducer needed for parallel updates

def search_source_a(state: ResearchState) -> dict:
    """Simulates a successful search."""
    return {
        "results": [f"Source A result for: {state['query']}"],
        "success_count": 1  # Return increment, reducer will sum
    }

def search_source_b(state: ResearchState) -> dict:
    """Simulates a failed search."""
    # This source is "down"
    return {
        "errors": ["Source B: Connection timeout"],
        "failure_count": 1  # Return increment, reducer will sum
    }

def search_source_c(state: ResearchState) -> dict:
    """Simulates another successful search."""
    return {
        "results": [f"Source C result for: {state['query']}"],
        "success_count": 1  # Return increment, reducer will sum
    }

def summarize_results(state: ResearchState) -> dict:
    """Summarize what we got."""
    print("\n=== Research Results ===")
    print(f"Successful sources: {state['success_count']}")
    print(f"Failed sources: {state['failure_count']}")
    
    if state["results"]:
        print("\nResults retrieved:")
        for r in state["results"]:
            print(f"  ✓ {r}")
    
    if state["errors"]:
        print("\nErrors encountered:")
        for e in state["errors"]:
            print(f"  ✗ {e}")
    
    return {}

# Build the graph
graph = StateGraph(ResearchState)

graph.add_node("source_a", search_source_a)
graph.add_node("source_b", search_source_b)
graph.add_node("source_c", search_source_c)
graph.add_node("summarize", summarize_results)

# All sources feed into summarize
graph.add_edge(START, "source_a")
graph.add_edge(START, "source_b")
graph.add_edge(START, "source_c")
graph.add_edge("source_a", "summarize")
graph.add_edge("source_b", "summarize")
graph.add_edge("source_c", "summarize")
graph.add_edge("summarize", END)

app = graph.compile()

# Run it
print("=== Graceful Degradation Demo ===")
result = app.invoke({
    "query": "AI agents",
    "results": [],
    "errors": [],
    "success_count": 0,
    "failure_count": 0
})