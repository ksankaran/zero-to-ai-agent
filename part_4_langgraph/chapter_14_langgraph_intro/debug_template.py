# From: Building AI Agents, Chapter 14, Section 14.7
# File: debug_template.py

"""Template for debug-ready LangGraph applications.

Use this as a starting point for new graphs that include
debugging from the start. Set DEBUG = False for production.
"""

import os
from typing import TypedDict, Annotated
from operator import add
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Debug flag - set to False in production
DEBUG = True


def debug_print(*args, **kwargs):
    """Print only if DEBUG is True."""
    if DEBUG:
        print(*args, **kwargs)


# === STATE ===

class MyState(TypedDict):
    input: str
    output: str
    step_count: int  # Track iterations


# === NODES (with debug output) ===

def my_node(state: MyState) -> dict:
    debug_print(f"\n🔵 my_node - Entered")
    debug_print(f"   Input: {state.get('input', 'N/A')[:50]}")
    
    # ... your logic here ...
    result = "processed"
    
    updates = {
        "output": result,
        "step_count": state.get("step_count", 0) + 1
    }
    
    debug_print(f"   Output: {result[:50]}")
    debug_print(f"   Step: {updates['step_count']}")
    
    return updates


# === ROUTING (with debug output) ===

def route_decision(state: MyState) -> str:
    decision = "end"  # Your logic here
    
    debug_print(f"🔀 route_decision: {decision}")
    
    return decision


# === GRAPH ===

def create_graph():
    graph = StateGraph(MyState)
    
    graph.add_node("my_node", my_node)
    graph.set_entry_point("my_node")
    
    graph.add_conditional_edges(
        "my_node",
        route_decision,
        {"continue": "my_node", "end": END}
    )
    
    return graph.compile()


# === MAIN ===

def main():
    app = create_graph()
    
    # Print graph structure
    if DEBUG:
        print("\n📊 Graph Structure:")
        print(app.get_graph().draw_mermaid())
    
    initial_state = {
        "input": "test input",
        "output": "",
        "step_count": 0
    }
    
    debug_print("\n🚀 Starting execution...")
    result = app.invoke(initial_state)
    
    debug_print(f"\n✅ Complete! Steps: {result['step_count']}")
    print(f"\nFinal output: {result['output']}")


if __name__ == "__main__":
    main()
