# From: Zero to AI Agent, Chapter 16, Section 16.6
# File: state_patterns.py

"""
Demonstrates the three state management patterns in LangGraph:
1. Replace - Agent overwrites a field completely
2. Accumulate - Agent adds to a list
3. Conditional Update - Agent updates only if needed
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
import operator


# =============================================================================
# PATTERN 1: REPLACE
# Agent overwrites a field completely
# =============================================================================

class ReplaceState(TypedDict):
    input_text: str
    processed_text: str  # Will be replaced each time


def processor_replace(state: ReplaceState) -> dict:
    """This REPLACES whatever was in 'processed_text'"""
    result = state["input_text"].upper()
    return {"processed_text": result}


# =============================================================================
# PATTERN 2: ACCUMULATE
# Agent adds to a list using Annotated with operator.add
# =============================================================================

class AccumulateState(TypedDict):
    items_to_process: list[str]
    results: Annotated[list[str], operator.add]  # Will accumulate


def processor_accumulate(state: AccumulateState) -> dict:
    """This APPENDS to the list, doesn't replace"""
    new_results = [item.upper() for item in state["items_to_process"]]
    return {"results": new_results}  # Gets added to existing results


def another_processor(state: AccumulateState) -> dict:
    """This also appends - both results are preserved"""
    new_results = [f"Processed: {item}" for item in state["items_to_process"]]
    return {"results": new_results}


# =============================================================================
# PATTERN 3: CONDITIONAL UPDATE
# Agent updates only if needed
# =============================================================================

class ConditionalState(TypedDict):
    value: int
    threshold: int
    exceeded: bool
    message: str


def conditional_checker(state: ConditionalState) -> dict:
    """Only updates fields when condition is met"""
    if state["value"] > state["threshold"]:
        return {
            "exceeded": True,
            "message": f"Value {state['value']} exceeds threshold {state['threshold']}"
        }
    # Return empty dict if no update needed - fields keep previous values
    return {}


# =============================================================================
# DEMONSTRATION
# =============================================================================

def demo_replace():
    """Demo the replace pattern"""
    print("=" * 50)
    print("PATTERN 1: REPLACE")
    print("=" * 50)
    
    workflow = StateGraph(ReplaceState)
    workflow.add_node("processor", processor_replace)
    workflow.add_edge(START, "processor")
    workflow.add_edge("processor", END)
    app = workflow.compile()
    
    result = app.invoke({
        "input_text": "hello world",
        "processed_text": ""
    })
    
    print(f"Input: 'hello world'")
    print(f"Output: '{result['processed_text']}'")
    print("(Field was replaced with new value)\n")


def demo_accumulate():
    """Demo the accumulate pattern"""
    print("=" * 50)
    print("PATTERN 2: ACCUMULATE")
    print("=" * 50)
    
    workflow = StateGraph(AccumulateState)
    workflow.add_node("proc1", processor_accumulate)
    workflow.add_node("proc2", another_processor)
    workflow.add_edge(START, "proc1")
    workflow.add_edge("proc1", "proc2")
    workflow.add_edge("proc2", END)
    app = workflow.compile()
    
    result = app.invoke({
        "items_to_process": ["a", "b", "c"],
        "results": []
    })
    
    print(f"Input items: ['a', 'b', 'c']")
    print(f"Accumulated results: {result['results']}")
    print("(Both processors' outputs are preserved)\n")


def demo_conditional():
    """Demo the conditional update pattern"""
    print("=" * 50)
    print("PATTERN 3: CONDITIONAL UPDATE")
    print("=" * 50)
    
    workflow = StateGraph(ConditionalState)
    workflow.add_node("checker", conditional_checker)
    workflow.add_edge(START, "checker")
    workflow.add_edge("checker", END)
    app = workflow.compile()
    
    # Test with value below threshold
    result1 = app.invoke({
        "value": 5,
        "threshold": 10,
        "exceeded": False,
        "message": "Initial"
    })
    print(f"Test 1: value=5, threshold=10")
    print(f"  exceeded: {result1['exceeded']}, message: '{result1['message']}'")
    print("  (No update - condition not met)")
    
    # Test with value above threshold
    result2 = app.invoke({
        "value": 15,
        "threshold": 10,
        "exceeded": False,
        "message": "Initial"
    })
    print(f"\nTest 2: value=15, threshold=10")
    print(f"  exceeded: {result2['exceeded']}, message: '{result2['message']}'")
    print("  (Updated - condition met)\n")


if __name__ == "__main__":
    demo_replace()
    demo_accumulate()
    demo_conditional()
    
    print("=" * 50)
    print("KEY TAKEAWAYS:")
    print("=" * 50)
    print("• REPLACE: Default behavior, last write wins")
    print("• ACCUMULATE: Use Annotated[list, operator.add]")
    print("• CONDITIONAL: Return empty dict {} to skip update")
