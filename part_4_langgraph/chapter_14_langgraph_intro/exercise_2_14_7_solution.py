# From: Building AI Agents, Chapter 14, Section 14.7
# File: exercise_2_14_7_solution.py

"""Fixed version of the buggy graph with debugging.

Exercise 2 Solution: Find and fix all the bugs in the provided code.

Bugs found and fixed:
1. results: list → results: Annotated[list, add] (so results accumulate)
2. state["search_count"] → state.get("search_count", 0) (KeyError fix)
3. Routing function returns must match mapping keys exactly
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, END


# BUG 1 FIX: Use Annotated[list, add] so results accumulate
class FixedState(TypedDict):
    query: str
    results: Annotated[list, add]  # FIXED: Was just 'list'
    search_count: int
    max_searches: int


def search(state: FixedState) -> dict:
    query = state["query"]
    
    # BUG 2 FIX: Use .get() with default value
    count = state.get("search_count", 0)  # FIXED: Was state["search_count"]
    
    print(f"🔍 Search #{count + 1}: {query}")
    
    result = f"Result for: {query}"
    
    return {
        "results": [result],  # This now accumulates thanks to Annotated
        "search_count": count + 1
    }


def should_continue(state: FixedState) -> str:
    """Fixed routing function with proper return values."""
    current = state.get("search_count", 0)
    maximum = state.get("max_searches", 3)
    
    print(f"🔀 Checking: {current} < {maximum}?")
    
    if current < maximum:
        # BUG 3 FIX: Return value must match mapping keys
        return "continue"  # FIXED: Was "search" which didn't match mapping
    return "done"  # FIXED: Was "end" which didn't match mapping


def create_fixed_graph():
    graph = StateGraph(FixedState)
    
    graph.add_node("search", search)
    graph.set_entry_point("search")
    
    # BUG 3 FIX: Mapping keys must match what routing function returns
    graph.add_conditional_edges(
        "search",
        should_continue,
        {
            "continue": "search",  # Loops back
            "done": END            # Exits
        }
    )
    
    return graph.compile()


def main():
    app = create_fixed_graph()
    
    print("🐛 Running fixed graph...")
    print("-" * 40)
    
    result = app.invoke({
        "query": "LangGraph tutorials",
        "results": [],          # Initialize empty list
        "search_count": 0,      # Initialize counter
        "max_searches": 3
    })
    
    print("-" * 40)
    print(f"✅ Total searches: {result['search_count']}")
    print(f"✅ Results collected: {len(result['results'])}")
    for i, r in enumerate(result['results'], 1):
        print(f"   {i}. {r}")


if __name__ == "__main__":
    main()


# === SUMMARY OF BUGS ===
"""
Bug 1: results: list should be results: Annotated[list, add]
  - Without Annotated, list gets replaced each time
  - With Annotated[list, add], lists accumulate across iterations

Bug 2: state["search_count"] throws KeyError if not initialized
  - Fixed with state.get("search_count", 0)
  - Always use .get() with defaults for safety

Bug 3: Routing function returned "search" and "end", but mapping had "continue" and "done"
  - The return values must EXACTLY match the mapping keys
  - This is a very common bug - always double-check your mapping!
"""
