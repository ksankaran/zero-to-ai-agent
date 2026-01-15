# From: Building AI Agents, Chapter 14, Section 14.5
# File: exercise_3_14_5_solution.py (Writer with Style Options)

"""Self-improving writer with style options.

Exercise 3: Add a style parameter (formal/casual/creative) that changes
how the writer creates and evaluates content.
"""

import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


# Style definitions
STYLES = {
    "formal": {
        "description": "professional, business-like, using industry terminology",
        "tone": "authoritative and polished",
        "example": "formal business report"
    },
    "casual": {
        "description": "friendly, conversational, approachable",
        "tone": "warm and relatable, like talking to a friend",
        "example": "blog post or social media"
    },
    "creative": {
        "description": "artistic, expressive, using vivid imagery",
        "tone": "imaginative and evocative",
        "example": "creative essay or storytelling"
    }
}


class WriterState(TypedDict):
    topic: str
    style: str                       # Writing style (formal/casual/creative)
    draft: str
    critique: str
    revision_count: int
    max_revisions: int


def get_style_prompt(style: str) -> str:
    """Get style instructions for prompts."""
    style_info = STYLES.get(style, STYLES["casual"])
    return f"""Style: {style_info['description']}
Tone: {style_info['tone']}
Write as if for: {style_info['example']}"""


def write_draft(state: WriterState) -> dict:
    """Write initial draft in the specified style."""
    topic = state["topic"]
    style = state["style"]
    style_instructions = get_style_prompt(style)
    
    prompt = f"""Write a short paragraph about: {topic}

{style_instructions}

Keep it to 3-4 sentences while maintaining the style throughout."""
    
    response = llm.invoke(prompt)
    
    print(f"📝 Draft written in {style} style")
    
    return {
        "draft": response.content,
        "revision_count": 0
    }


def critique_draft(state: WriterState) -> dict:
    """Critique with style considerations."""
    draft = state["draft"]
    topic = state["topic"]
    style = state["style"]
    style_info = STYLES.get(style, STYLES["casual"])
    
    prompt = f"""Review this {style} draft about "{topic}".
    
    Draft:
    {draft}
    
    The intended style is: {style_info['description']}
    The intended tone is: {style_info['tone']}
    
    Evaluate:
    1. Does it match the intended style and tone?
    2. Is the content accurate and engaging?
    3. What specific improvements would make it better?
    
    If it's excellent for the style, say "EXCELLENT" at the start."""
    
    response = llm.invoke(prompt)
    
    print(f"🔍 Critique for {style} style provided")
    
    return {"critique": response.content}


def revise_draft(state: WriterState) -> dict:
    """Revise while maintaining style."""
    draft = state["draft"]
    critique = state["critique"]
    topic = state["topic"]
    style = state["style"]
    style_instructions = get_style_prompt(style)
    revision_count = state["revision_count"]
    
    prompt = f"""Revise this draft about "{topic}" based on feedback.

{style_instructions}

Current draft:
{draft}

Feedback:
{critique}

Write an improved version that addresses the feedback while maintaining the {style} style."""
    
    response = llm.invoke(prompt)
    
    new_count = revision_count + 1
    print(f"✏️ Revision {new_count} complete")
    
    return {
        "draft": response.content,
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
    print("=" * 50)
    print("🎨 Styled Self-Improving Writer")
    print("=" * 50)
    
    # Get topic
    topic = input("\n📝 Topic to write about:\n> ").strip()
    if not topic:
        topic = "The value of continuous learning"
    
    # Get style
    print("\n🎨 Available styles:")
    for style, info in STYLES.items():
        print(f"  - {style}: {info['description']}")
    
    style = input("\nChoose style (formal/casual/creative):\n> ").strip().lower()
    if style not in STYLES:
        style = "casual"
        print(f"(Using default: {style})")
    
    # Run for chosen style
    app = create_graph()
    
    result = app.invoke({
        "topic": topic,
        "style": style,
        "draft": "",
        "critique": "",
        "revision_count": 0,
        "max_revisions": 2
    })
    
    print("\n" + "=" * 50)
    print(f"📄 FINAL DRAFT ({style.upper()} STYLE):")
    print("=" * 50)
    print(result["draft"])
    
    # Bonus: Compare all three styles
    compare = input("\n\nCompare all three styles on same topic? (y/n): ").strip().lower()
    if compare == 'y':
        print("\n" + "=" * 50)
        print("🎨 STYLE COMPARISON")
        print("=" * 50)
        
        for style_name in STYLES:
            print(f"\n--- {style_name.upper()} ---")
            result = app.invoke({
                "topic": topic,
                "style": style_name,
                "draft": "",
                "critique": "",
                "revision_count": 0,
                "max_revisions": 1  # Just 1 revision for speed
            })
            print(result["draft"])


if __name__ == "__main__":
    main()
