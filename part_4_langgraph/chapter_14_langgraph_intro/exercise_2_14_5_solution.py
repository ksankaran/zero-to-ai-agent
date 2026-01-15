# From: Building AI Agents, Chapter 14, Section 14.5
# File: exercise_2_14_5_solution.py (Writer with Quality Scoring)

"""Self-improving writer with quality scoring.

Exercise 2: Add a numeric quality score (1-10) to the process.
The writer continues until the score reaches 8 or higher.
"""

import os
import re
from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


class WriterState(TypedDict):
    topic: str
    draft: str
    critique: str
    quality_score: int               # Numeric quality score (1-10)
    score_history: list              # Track scores over time
    revision_count: int
    max_revisions: int


def write_draft(state: WriterState) -> dict:
    """Write the initial draft."""
    topic = state["topic"]
    
    prompt = f"""Write a short, informative paragraph about: {topic}
    Keep it concise but engaging. Aim for 3-4 sentences."""
    
    response = llm.invoke(prompt)
    
    print(f"📝 Draft written")
    
    return {
        "draft": response.content,
        "revision_count": 0,
        "quality_score": 0,
        "score_history": []
    }


def critique_draft(state: WriterState) -> dict:
    """Critique and score the draft."""
    draft = state["draft"]
    topic = state["topic"]
    
    prompt = f"""Review this draft about "{topic}".
    
    Draft:
    {draft}
    
    Provide:
    1. A quality score from 1-10 (format: "SCORE: X")
    2. Brief feedback for improvement
    
    Be a tough but fair critic. Only give 9-10 for truly excellent writing."""
    
    response = llm.invoke(prompt)
    critique_text = response.content
    
    # Extract score from response
    score_match = re.search(r'SCORE:\s*(\d+)', critique_text, re.IGNORECASE)
    score = int(score_match.group(1)) if score_match else 5
    score = max(1, min(10, score))  # Clamp to 1-10
    
    # Update score history
    new_history = state.get("score_history", []) + [score]
    
    print(f"🔍 Critique: Score {score}/10")
    
    return {
        "critique": critique_text,
        "quality_score": score,
        "score_history": new_history
    }


def revise_draft(state: WriterState) -> dict:
    """Revise based on feedback."""
    draft = state["draft"]
    critique = state["critique"]
    topic = state["topic"]
    revision_count = state["revision_count"]
    
    prompt = f"""Revise this draft about "{topic}" based on feedback:
    
    Current draft: {draft}
    Feedback: {critique}
    
    Write an improved version that addresses the feedback."""
    
    response = llm.invoke(prompt)
    
    new_count = revision_count + 1
    print(f"✏️ Revision {new_count} complete")
    
    return {
        "draft": response.content,
        "revision_count": new_count
    }


def should_continue(state: WriterState) -> str:
    """Decide based on score and revision count."""
    score = state["quality_score"]
    revision_count = state["revision_count"]
    max_revisions = state["max_revisions"]
    
    # Stop if score is 8 or higher
    if score >= 8:
        print(f"✨ Quality score {score}/10 - excellent!")
        return "end"
    
    # Stop if max revisions reached
    if revision_count >= max_revisions:
        print(f"🛑 Max revisions reached (score: {score}/10)")
        return "end"
    
    print(f"🔄 Score {score}/10 - continuing...")
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
        "topic": "The importance of sleep for health",
        "draft": "",
        "critique": "",
        "quality_score": 0,
        "score_history": [],
        "revision_count": 0,
        "max_revisions": 3
    })
    
    print("\n" + "=" * 50)
    print("📄 FINAL DRAFT:")
    print("=" * 50)
    print(result["draft"])
    
    print("\n" + "-" * 50)
    print(f"📊 Score progression: {' → '.join(map(str, result['score_history']))}")
    print(f"📊 Final score: {result['quality_score']}/10")
    print(f"📊 Total revisions: {result['revision_count']}")


if __name__ == "__main__":
    main()
