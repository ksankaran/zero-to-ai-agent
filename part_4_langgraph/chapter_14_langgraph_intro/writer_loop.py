# From: Building AI Agents, Chapter 14, Section 14.4
# File: writer_loop.py

"""
A simple feedback loop demonstrating LangGraph core concepts:
- State with TypedDict
- Nodes that read/write state
- Conditional edges for looping
- The add reducer for list accumulation
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, END


# 1. Define our state
class WriterState(TypedDict):
    topic: str                           # What to write about
    drafts: Annotated[list, add]         # Accumulate drafts
    current_draft: str                   # Latest draft
    quality_score: int                   # How good is it (1-10)


# 2. Define our nodes
def write_draft(state: WriterState) -> dict:
    """Write or rewrite a draft."""
    topic = state["topic"]
    attempt = len(state.get("drafts", [])) + 1
    
    # In reality, this would call an LLM
    draft = f"Draft {attempt} about {topic}: [content here]"
    
    return {
        "current_draft": draft,
        "drafts": [draft]  # Appends due to Annotated[list, add]
    }


def evaluate_draft(state: WriterState) -> dict:
    """Score the current draft."""
    draft = state["current_draft"]
    
    # In reality, this would use an LLM or other logic
    # For demo, score increases with each attempt
    score = min(len(state.get("drafts", [])) * 3, 10)
    
    return {"quality_score": score}


def decide_if_done(state: WriterState) -> str:
    """Decide whether to finish or revise."""
    if state["quality_score"] >= 7:
        return "done"
    elif len(state.get("drafts", [])) >= 3:
        return "done"  # Give up after 3 attempts
    else:
        return "revise"


# 3. Build the graph
graph = StateGraph(WriterState)

# Add nodes
graph.add_node("write", write_draft)
graph.add_node("evaluate", evaluate_draft)

# Add edges
graph.set_entry_point("write")
graph.add_edge("write", "evaluate")
graph.add_conditional_edges(
    "evaluate",
    decide_if_done,
    {
        "done": END,
        "revise": "write"  # Loop back!
    }
)

# 4. Compile the graph
app = graph.compile()

# 5. Run it!
if __name__ == "__main__":
    result = app.invoke({"topic": "AI agents", "drafts": []})
    print(f"Final draft: {result['current_draft']}")
    print(f"Total attempts: {len(result['drafts'])}")
    print(f"Final score: {result['quality_score']}")
    
    # Show all drafts
    print("\nAll drafts:")
    for i, draft in enumerate(result['drafts'], 1):
        print(f"  {i}. {draft}")
