# From: Zero to AI Agent, Chapter 16, Section 16.6
# File: parallel_state_handling.py

"""
Demonstrates how to handle state correctly when agents run in parallel.

Problem: When two agents write to the same field, LangGraph raises an error.
Solutions shown:
1. Separate fields for each agent
2. Accumulate into a shared list
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
import operator


# =============================================================================
# THE PROBLEM: Both agents write to same field
# =============================================================================

class BadState(TypedDict):
    data: str
    result: str  # PROBLEM: Both agents write here!


def agent_a_bad(state: BadState) -> dict:
    return {"result": f"Agent A analyzed: {state['data'][:20]}"}


def agent_b_bad(state: BadState) -> dict:
    return {"result": f"Agent B analyzed: {state['data'][:20]}"}  # Conflict!


def demo_problem():
    """Show the problem with parallel agents writing to same field"""
    print("=" * 60)
    print("PROBLEM: Parallel agents writing to same field")
    print("=" * 60)
    
    workflow = StateGraph(BadState)
    workflow.add_node("agent_a", agent_a_bad)
    workflow.add_node("agent_b", agent_b_bad)
    
    # Both run in parallel from START
    workflow.add_edge(START, "agent_a")
    workflow.add_edge(START, "agent_b")
    workflow.add_edge("agent_a", END)
    workflow.add_edge("agent_b", END)
    
    app = workflow.compile()
    
    try:
        result = app.invoke({
            "data": "Some text to analyze",
            "result": ""
        })
        # Old behavior (silent overwrite)
        print(f"Result: '{result['result']}'")
        print("⚠️  Only ONE agent's result is preserved!")
        print("   The other was overwritten.\n")
    except Exception as e:
        # New behavior (LangGraph catches the conflict)
        print(f"\n❌ LangGraph caught the conflict!")
        print(f"   Error: {type(e).__name__}")
        print(f"   Message: Can receive only one value per step.")
        print("\n✅ This is actually GOOD - LangGraph prevents data loss!")
        print("   Let's see how to fix it properly...\n")


# =============================================================================
# SOLUTION 1: Separate fields for each agent
# =============================================================================

class SeparateFieldsState(TypedDict):
    data: str
    result_a: str  # Agent A owns this
    result_b: str  # Agent B owns this
    combined: str  # Merger owns this


def agent_a_separate(state: SeparateFieldsState) -> dict:
    return {"result_a": f"Agent A: {state['data'][:20]}..."}


def agent_b_separate(state: SeparateFieldsState) -> dict:
    return {"result_b": f"Agent B: {state['data'][:20]}..."}


def merger_separate(state: SeparateFieldsState) -> dict:
    return {"combined": f"{state['result_a']}\n{state['result_b']}"}


def demo_solution_1():
    """Demo solution with separate fields"""
    print("=" * 60)
    print("SOLUTION 1: Separate fields for each agent")
    print("=" * 60)
    
    workflow = StateGraph(SeparateFieldsState)
    workflow.add_node("agent_a", agent_a_separate)
    workflow.add_node("agent_b", agent_b_separate)
    workflow.add_node("merger", merger_separate)
    
    # Parallel execution
    workflow.add_edge(START, "agent_a")
    workflow.add_edge(START, "agent_b")
    
    # Both feed into merger
    workflow.add_edge("agent_a", "merger")
    workflow.add_edge("agent_b", "merger")
    
    workflow.add_edge("merger", END)
    
    app = workflow.compile()
    
    result = app.invoke({
        "data": "Some text to analyze for demonstration",
        "result_a": "",
        "result_b": "",
        "combined": ""
    })
    
    print(f"Agent A result: '{result['result_a']}'")
    print(f"Agent B result: '{result['result_b']}'")
    print(f"Combined: '{result['combined']}'")
    print("✅ Both results preserved!\n")


# =============================================================================
# SOLUTION 2: Accumulate into a shared list
# =============================================================================

class AccumulateState(TypedDict):
    data: str
    results: Annotated[list[str], operator.add]  # Both agents add to this


def agent_a_accumulate(state: AccumulateState) -> dict:
    return {"results": [f"Agent A: {state['data'][:20]}..."]}


def agent_b_accumulate(state: AccumulateState) -> dict:
    return {"results": [f"Agent B: {state['data'][:20]}..."]}


def demo_solution_2():
    """Demo solution with accumulation"""
    print("=" * 60)
    print("SOLUTION 2: Accumulate into a shared list")
    print("=" * 60)
    
    workflow = StateGraph(AccumulateState)
    workflow.add_node("agent_a", agent_a_accumulate)
    workflow.add_node("agent_b", agent_b_accumulate)
    
    # Parallel execution
    workflow.add_edge(START, "agent_a")
    workflow.add_edge(START, "agent_b")
    workflow.add_edge("agent_a", END)
    workflow.add_edge("agent_b", END)
    
    app = workflow.compile()
    
    result = app.invoke({
        "data": "Some text to analyze for demonstration",
        "results": []
    })
    
    print(f"Accumulated results: {result['results']}")
    print("✅ Both results preserved in list!\n")


# =============================================================================
# BEST PRACTICE: Clear field ownership
# =============================================================================

def show_ownership_pattern():
    """Show the ownership pattern we use"""
    print("=" * 60)
    print("BEST PRACTICE: Clear field ownership")
    print("=" * 60)
    print("""
In our research team (Section 16.5):

    Agent          | Owns Field      | Reads From
    ---------------|-----------------|------------------
    Planner        | questions       | topic
    Researcher     | findings        | questions
    Analyst        | insights        | findings
    Writer         | report          | insights, findings
    Reviewer       | approved, feedback | report

No conflicts because each agent writes to different fields!
""")


if __name__ == "__main__":
    demo_problem()
    demo_solution_1()
    demo_solution_2()
    show_ownership_pattern()