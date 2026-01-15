# From: Building AI Agents, Chapter 14, Section 14.3
# File: verify_langgraph.py

"""Verify LangGraph components are accessible."""

def check_langgraph():
    """Check that we can import LangGraph components."""
    print("🔍 Checking LangGraph components...\n")
    
    try:
        # Core graph components
        from langgraph.graph import StateGraph, END
        print("✅ StateGraph imported (for building graphs)")
        print("✅ END imported (for marking end states)")
        
        # State management
        from typing import TypedDict
        print("✅ TypedDict available (for defining state)")
        
        # Checkpointing (for persistence)
        from langgraph.checkpoint.memory import MemorySaver
        print("✅ MemorySaver imported (for state persistence)")
        
        print("\n🎉 All LangGraph components ready!")
        print("\nYou can now build graphs with:")
        print("  - StateGraph: Define your graph structure")
        print("  - Nodes: Add processing steps")
        print("  - Edges: Connect steps together")
        print("  - State: Share data between nodes")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

if __name__ == "__main__":
    check_langgraph()
