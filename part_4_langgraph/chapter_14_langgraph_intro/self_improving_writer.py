# From: Building AI Agents, Chapter 14, Section 14.5
# File: self_improving_writer.py

"""A LangGraph application that writes and improves content iteratively.

This demonstrates the fundamental generate → evaluate → improve → repeat pattern
used in many AI agents.
"""

import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# Initialize our LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


# === STATE ===

class WriterState(TypedDict):
    topic: str                    # The topic to write about
    draft: str                    # Current draft
    critique: str                 # Feedback on the draft
    revision_count: int           # How many revisions so far
    max_revisions: int            # Maximum revisions allowed


# === NODES ===

def write(state: WriterState) -> dict:
    """Write or revise the draft based on current state."""
    topic = state["topic"]
    draft = state.get("draft", "")
    critique = state.get("critique", "")
    revision_count = state.get("revision_count", 0)

    if not draft:
        # Initial draft - no existing content
        prompt = f"""Write a short, informative paragraph about: {topic}

        Keep it concise but engaging. Aim for 3-4 sentences."""

        response = llm.invoke(prompt)
        print(f"📝 Initial draft written ({len(response.content)} chars)")

        return {
            "draft": response.content,
            "revision_count": 0
        }
    else:
        # Revision - improve based on critique
        prompt = f"""Revise this draft about "{topic}" based on the feedback provided.

        Current draft:
        {draft}

        Feedback:
        {critique}

        Write an improved version that addresses the feedback. Keep it concise."""

        response = llm.invoke(prompt)
        new_count = revision_count + 1
        print(f"✏️ Revision {new_count} complete")

        return {
            "draft": response.content,
            "revision_count": new_count
        }


def critique_draft(state: WriterState) -> dict:
    """Analyze the draft and provide constructive feedback."""
    draft = state["draft"]
    topic = state["topic"]

    prompt = f"""Review this draft about "{topic}" and provide brief, constructive feedback.

    Draft:
    {draft}

    Focus on:
    1. Is the information accurate and complete?
    2. Is it engaging and well-written?
    3. What specific improvements would make it better?

    If the draft is already excellent, say "EXCELLENT" at the start of your response.
    Otherwise, provide 2-3 specific suggestions for improvement."""

    response = llm.invoke(prompt)

    print(f"🔍 Critique: {response.content[:100]}...")

    return {"critique": response.content}


# === DECISION FUNCTION ===

def should_continue(state: WriterState) -> str:
    """Decide whether to revise again or finish."""
    critique = state["critique"]
    revision_count = state["revision_count"]
    max_revisions = state["max_revisions"]
    
    # Stop if we've hit the revision limit
    if revision_count >= max_revisions:
        print(f"🛑 Max revisions ({max_revisions}) reached")
        return "end"
    
    # Stop if the critique says it's excellent
    if "EXCELLENT" in critique.upper():
        print("✨ Draft deemed excellent!")
        return "end"
    
    # Otherwise, keep improving
    print("🔄 Continuing to revise...")
    return "continue"


# === GRAPH BUILDER ===

def create_writer_graph():
    """Build and return the writer graph."""

    # Create the graph with our state type
    graph = StateGraph(WriterState)

    # Add our nodes
    graph.add_node("write", write)
    graph.add_node("critique", critique_draft)

    # Set the entry point
    graph.set_entry_point("write")

    # Add edges
    graph.add_edge("write", "critique")

    graph.add_conditional_edges(
        "critique",
        should_continue,
        {
            "continue": "write",  # Loop back to write for revision
            "end": END
        }
    )

    return graph.compile()


# === MAIN ===

def main():
    """Run the self-improving writer."""
    print("=" * 50)
    print("🚀 Self-Improving Writer")
    print("=" * 50)
    
    # Create the graph
    app = create_writer_graph()
    
    # Define our initial state
    initial_state = {
        "topic": "Why learning to code is valuable in 2024",
        "draft": "",
        "critique": "",
        "revision_count": 0,
        "max_revisions": 3
    }
    
    print(f"\n📌 Topic: {initial_state['topic']}")
    print(f"📌 Max revisions: {initial_state['max_revisions']}")
    print("\n" + "-" * 50 + "\n")
    
    # Run the graph
    result = app.invoke(initial_state)
    
    # Show the final result
    print("\n" + "=" * 50)
    print("📄 FINAL DRAFT:")
    print("=" * 50)
    print(result["draft"])
    print("\n" + "-" * 50)
    print(f"Total revisions: {result['revision_count']}")


if __name__ == "__main__":
    main()
