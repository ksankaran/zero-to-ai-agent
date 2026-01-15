# From: Zero to AI Agent, Chapter 16, Section 16.6
# File: exercise_2_16_6_solution.py

"""
Exercise 2 Solution: Fix the Bug

Problem: Two parallel agents both write to the same "result" field,
causing a conflict. LangGraph catches this and raises an error.

This file demonstrates:
1. The problem (LangGraph raises InvalidUpdateError)
2. Solution 1: Separate fields
3. Solution 2: Accumulate into a list
4. Solution 3: Separate fields + Merger
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
import operator


# =============================================================================
# THE PROBLEM
# =============================================================================

class BadState(TypedDict):
    data: str
    result: str  # PROBLEM: Both analyzers write here!


def technical_analyzer_bad(state: BadState) -> dict:
    """Technical analysis - writes to 'result'."""
    return {"result": f"Technical: Data shows patterns in {state['data'][:20]}..."}


def business_analyzer_bad(state: BadState) -> dict:
    """Business analysis - ALSO writes to 'result' - CONFLICT!"""
    return {"result": f"Business: Market implications of {state['data'][:20]}..."}


def demo_problem():
    """Demonstrate the conflict problem."""
    print("=" * 60)
    print("THE PROBLEM: Both agents write to same field")
    print("=" * 60)
    
    workflow = StateGraph(BadState)
    workflow.add_node("technical", technical_analyzer_bad)
    workflow.add_node("business", business_analyzer_bad)
    
    # Both run in parallel
    workflow.add_edge(START, "technical")
    workflow.add_edge(START, "business")
    workflow.add_edge("technical", END)
    workflow.add_edge("business", END)
    
    app = workflow.compile()
    
    try:
        result = app.invoke({
            "data": "Q3 sales increased by 15% with strong tech sector growth",
            "result": ""
        })
        # In older LangGraph versions, one result would silently overwrite
        print(f"\nResult field: {result['result']}")
        print("\n⚠️  Only ONE analysis is preserved - the other was overwritten!")
    except Exception as e:
        # In newer LangGraph versions, this raises InvalidUpdateError (good!)
        print(f"\n❌ LangGraph caught the conflict!")
        print(f"   Error: {type(e).__name__}")
        print(f"   Message: Can receive only one value per step.")
        print("\n✅ This is actually GOOD - LangGraph prevents the bug!")
        print("   Now let's see how to fix it properly...")


# =============================================================================
# SOLUTION 1: Separate Fields
# =============================================================================

class SeparateFieldsState(TypedDict):
    data: str
    technical_result: str  # Technical analyzer owns this
    business_result: str   # Business analyzer owns this


def technical_analyzer_v1(state: SeparateFieldsState) -> dict:
    """Technical analysis - writes to its own field."""
    return {"technical_result": f"Technical: Data shows patterns in {state['data'][:20]}..."}


def business_analyzer_v1(state: SeparateFieldsState) -> dict:
    """Business analysis - writes to its own field."""
    return {"business_result": f"Business: Market implications of {state['data'][:20]}..."}


def demo_solution_1():
    """Demonstrate Solution 1: Separate fields."""
    print("\n" + "=" * 60)
    print("SOLUTION 1: Separate fields for each agent")
    print("=" * 60)
    
    workflow = StateGraph(SeparateFieldsState)
    workflow.add_node("technical", technical_analyzer_v1)
    workflow.add_node("business", business_analyzer_v1)
    
    # Both run in parallel
    workflow.add_edge(START, "technical")
    workflow.add_edge(START, "business")
    workflow.add_edge("technical", END)
    workflow.add_edge("business", END)
    
    app = workflow.compile()
    
    result = app.invoke({
        "data": "Q3 sales increased by 15% with strong tech sector growth",
        "technical_result": "",
        "business_result": ""
    })
    
    print(f"\nTechnical result: {result['technical_result']}")
    print(f"Business result: {result['business_result']}")
    print("\n✅ Both results preserved!")


# =============================================================================
# SOLUTION 2: Accumulate into a List
# =============================================================================

class AccumulateState(TypedDict):
    data: str
    results: Annotated[list[str], operator.add]  # Both add to this list


def technical_analyzer_v2(state: AccumulateState) -> dict:
    """Technical analysis - appends to shared list."""
    return {"results": [f"Technical: Data shows patterns in {state['data'][:20]}..."]}


def business_analyzer_v2(state: AccumulateState) -> dict:
    """Business analysis - appends to shared list."""
    return {"results": [f"Business: Market implications of {state['data'][:20]}..."]}


def demo_solution_2():
    """Demonstrate Solution 2: Accumulate into list."""
    print("\n" + "=" * 60)
    print("SOLUTION 2: Accumulate into a shared list")
    print("=" * 60)
    
    workflow = StateGraph(AccumulateState)
    workflow.add_node("technical", technical_analyzer_v2)
    workflow.add_node("business", business_analyzer_v2)
    
    # Both run in parallel
    workflow.add_edge(START, "technical")
    workflow.add_edge(START, "business")
    workflow.add_edge("technical", END)
    workflow.add_edge("business", END)
    
    app = workflow.compile()
    
    result = app.invoke({
        "data": "Q3 sales increased by 15% with strong tech sector growth",
        "results": []
    })
    
    print(f"\nAccumulated results:")
    for i, r in enumerate(result['results'], 1):
        print(f"  {i}. {r}")
    print("\n✅ Both results preserved in list!")


# =============================================================================
# SOLUTION 3: Separate Fields + Merger
# =============================================================================

class MergerState(TypedDict):
    data: str
    technical_result: str
    business_result: str
    combined: str  # Merger fills this


def technical_analyzer_v3(state: MergerState) -> dict:
    return {"technical_result": f"Technical: Patterns in {state['data'][:20]}..."}


def business_analyzer_v3(state: MergerState) -> dict:
    return {"business_result": f"Business: Implications of {state['data'][:20]}..."}


def merger(state: MergerState) -> dict:
    """Combines both analyses into a single result."""
    combined = f"""COMBINED ANALYSIS:

{state['technical_result']}

{state['business_result']}"""
    return {"combined": combined}


def demo_solution_3():
    """Demonstrate Solution 3: Separate fields with merger."""
    print("\n" + "=" * 60)
    print("SOLUTION 3: Separate fields + Merger agent")
    print("=" * 60)
    
    workflow = StateGraph(MergerState)
    workflow.add_node("technical", technical_analyzer_v3)
    workflow.add_node("business", business_analyzer_v3)
    workflow.add_node("merger", merger)
    
    # Both run in parallel
    workflow.add_edge(START, "technical")
    workflow.add_edge(START, "business")
    
    # Both feed into merger
    workflow.add_edge("technical", "merger")
    workflow.add_edge("business", "merger")
    
    workflow.add_edge("merger", END)
    
    app = workflow.compile()
    
    result = app.invoke({
        "data": "Q3 sales increased by 15% with strong tech sector growth",
        "technical_result": "",
        "business_result": "",
        "combined": ""
    })
    
    print(f"\n{result['combined']}")
    print("\n✅ Both results combined by merger!")


# =============================================================================
# RUN ALL DEMOS
# =============================================================================

if __name__ == "__main__":
    demo_problem()
    demo_solution_1()
    demo_solution_2()
    demo_solution_3()
    
    print("\n" + "=" * 60)
    print("SUMMARY: Which solution to choose?")
    print("=" * 60)
    print("""
Solution 1 (Separate fields):
  + Best when you need to access results individually
  + Clear ownership of each field
  + Easy to debug

Solution 2 (Accumulate list):
  + Best when number of agents is dynamic
  + Easy to iterate over all results
  + Works with any number of parallel agents

Solution 3 (Separate + Merger):
  + Best when you need both individual AND combined access
  + Merger can do intelligent synthesis
  + Most flexible but adds complexity
""")