# From: Building AI Agents, Chapter 14, Section 14.5
# File: exercise_1_14_5_solution.py (Writer with Draft History)

"""Self-improving writer that keeps history of all drafts.

Exercise 1: Modify the writer to keep a history of all drafts using
Annotated[list, add] so you can see how the writing evolved.
"""

import os
from typing import TypedDict, Annotated
from operator import add
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


class WriterState(TypedDict):
    topic: str
    drafts: Annotated[list, add]     # History of all drafts
    current_draft: str                # Most recent draft
    critique: str
    revision_count: int
    max_revisions: int


def write_draft(state: WriterState) -> dict:
    """Write the initial draft."""
    topic = state["topic"]
    
    prompt = f"""Write a short, informative paragraph about: {topic}
    Keep it concise but engaging. Aim for 3-4 sentences."""
    
    response = llm.invoke(prompt)
    draft = response.content
    
    print(f"📝 Draft written ({len(draft)} chars)")
    
    return {
        "current_draft": draft,
        "drafts": [{"version": 1, "content": draft}],  # Appends to list
        "revision_count": 0
    }


def critique_draft(state: WriterState) -> dict:
    """Critique the current draft."""
    draft = state["current_draft"]
    topic = state["topic"]
    
    prompt = f"""Review this draft about "{topic}" and provide brief feedback.
    
    Draft:
    {draft}
    
    If excellent, say "EXCELLENT" at the start. Otherwise give 2-3 suggestions."""
    
    response = llm.invoke(prompt)
    print(f"🔍 Critique provided")
    
    return {"critique": response.content}


def revise_draft(state: WriterState) -> dict:
    """Revise based on feedback."""
    draft = state["current_draft"]
    critique = state["critique"]
    topic = state["topic"]
    revision_count = state["revision_count"]
    
    prompt = f"""Revise this draft about "{topic}" based on feedback:
    
    Current draft: {draft}
    Feedback: {critique}
    
    Write an improved version."""
    
    response = llm.invoke(prompt)
    new_draft = response.content
    new_count = revision_count + 1
    
    print(f"✏️ Revision {new_count} complete")
    
    return {
        "current_draft": new_draft,
        "drafts": [{"version": new_count + 1, "content": new_draft}],  # Appends
        "revision_count": new_count
    }


def should_continue(state: WriterState) -> str:
    """Decide whether to continue revising."""
    if state["revision_count"] >= state["max_revisions"]:
        return "end"
    if "EXCELLENT" in state["critique"].upper():
        return "end"
    return "revise"


def create_graph():
    graph = StateGraph(WriterState)
    
    graph.add_node("write_draft", write_draft)
    graph.add_node("critique", critique_draft)
    graph.add_node("revise", revise_draft)
    
    graph.set_entry_point("write_draft")
    graph.add_edge("write_draft", "critique")
    graph.add_conditional_edges("critique", should_continue, {"revise": "revise", "end": END})
    graph.add_edge("revise", "critique")
    
    return graph.compile()


def main():
    app = create_graph()
    
    result = app.invoke({
        "topic": "The benefits of reading books",
        "drafts": [],
        "current_draft": "",
        "critique": "",
        "revision_count": 0,
        "max_revisions": 3
    })
    
    # Display all versions
    print("\n" + "=" * 50)
    print("📚 DRAFT HISTORY:")
    print("=" * 50)
    
    for draft in result["drafts"]:
        print(f"\n--- Version {draft['version']} ---")
        print(draft["content"])
    
    print("\n" + "=" * 50)
    print(f"Total versions: {len(result['drafts'])}")


if __name__ == "__main__":
    main()
