# From: Building AI Agents, Chapter 14, Section 14.6
# File: content_moderator.py

"""Content moderation with sequential decision gates.

Demonstrates Pattern 2: Chained Decisions
- Safety check → Topic check → Quality check
- Each gate can reject or pass to next
- Fail fast on safety violations
"""

import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


# === STATE ===

class ModerationState(TypedDict):
    content: str              # Content to moderate
    is_safe: bool             # Passes safety check?
    is_on_topic: bool         # Relevant to platform?
    quality_score: int        # Content quality (1-10)
    decision: str             # Final decision
    reason: str               # Explanation for the decision


# === GATE 1: SAFETY CHECK ===

def check_safety(state: ModerationState) -> dict:
    """First gate: Check for harmful content.
    
    This runs FIRST because there's no point checking topic or quality
    if the content is unsafe. We fail fast on safety violations.
    """
    content = state["content"]
    
    prompt = f"""Is this content safe and appropriate? Check for:
    - Hate speech or discrimination
    - Violence or threats
    - Adult content
    - Spam or scams
    
    Content: {content}
    
    Respond with only: SAFE or UNSAFE"""
    
    response = llm.invoke(prompt)
    is_safe = "SAFE" in response.content.upper() and "UNSAFE" not in response.content.upper()
    
    print(f"🛡️ Safety check: {'PASS' if is_safe else 'FAIL'}")
    
    return {"is_safe": is_safe}


def route_after_safety(state: ModerationState) -> str:
    """Route based on safety check result."""
    if state["is_safe"]:
        return "check_topic"      # Continue to next gate
    else:
        return "reject_unsafe"    # Stop here, reject immediately


# === GATE 2: TOPIC RELEVANCE ===

def check_topic(state: ModerationState) -> dict:
    """Second gate: Check if content is on-topic.
    
    We only reach here if safety passed. Now we check if
    the content belongs on our technology forum.
    """
    content = state["content"]
    
    prompt = f"""Is this content relevant to a technology discussion forum?
    
    Content: {content}
    
    Respond with only: ON_TOPIC or OFF_TOPIC"""
    
    response = llm.invoke(prompt)
    is_on_topic = "ON_TOPIC" in response.content.upper()
    
    print(f"🎯 Topic check: {'PASS' if is_on_topic else 'FAIL'}")
    
    return {"is_on_topic": is_on_topic}


def route_after_topic(state: ModerationState) -> str:
    """Route based on topic relevance."""
    if state["is_on_topic"]:
        return "check_quality"     # Continue to final gate
    else:
        return "reject_off_topic"  # Wrong forum


# === GATE 3: QUALITY ASSESSMENT ===

def check_quality(state: ModerationState) -> dict:
    """Third gate: Assess content quality.
    
    Safe, on-topic content still needs to meet quality standards.
    We use a 1-10 score for nuanced decisions:
    - 7-10: Approve
    - 4-6: Approve with suggestions
    - 1-3: Reject for low quality
    """
    content = state["content"]
    
    prompt = f"""Rate this content's quality from 1-10 based on:
    - Clarity and coherence
    - Usefulness to others
    - Effort and thoughtfulness
    
    Content: {content}
    
    Respond with only a number 1-10."""
    
    response = llm.invoke(prompt)
    
    # Parse the score with fallback
    try:
        score = int(''.join(filter(str.isdigit, response.content)))
        score = max(1, min(10, score))  # Clamp to valid range
    except:
        score = 5  # Default if parsing fails
    
    print(f"⭐ Quality score: {score}/10")
    
    return {"quality_score": score}


def route_after_quality(state: ModerationState) -> str:
    """Route based on quality score."""
    score = state["quality_score"]
    
    if score >= 7:
        return "approve"
    elif score >= 4:
        return "approve_with_note"
    else:
        return "reject_low_quality"


# === TERMINAL NODES ===

def approve(state: ModerationState) -> dict:
    """Approve high-quality content."""
    print("✅ Content approved!")
    return {
        "decision": "APPROVED",
        "reason": "Content meets all quality standards."
    }


def approve_with_note(state: ModerationState) -> dict:
    """Approve but suggest improvements."""
    print("✅ Content approved with suggestions")
    return {
        "decision": "APPROVED_WITH_SUGGESTIONS",
        "reason": f"Content approved. Quality: {state['quality_score']}/10. Consider adding more detail."
    }


def reject_unsafe(state: ModerationState) -> dict:
    """Reject content that failed safety check."""
    print("❌ Rejected: Safety violation")
    return {
        "decision": "REJECTED",
        "reason": "Content violates community safety guidelines."
    }


def reject_off_topic(state: ModerationState) -> dict:
    """Reject content that's not relevant."""
    print("❌ Rejected: Off-topic")
    return {
        "decision": "REJECTED",
        "reason": "Content is not relevant to this forum."
    }


def reject_low_quality(state: ModerationState) -> dict:
    """Reject content that failed quality check."""
    print("❌ Rejected: Low quality")
    return {
        "decision": "REJECTED",
        "reason": "Content does not meet quality standards. Please add more detail."
    }


# === GRAPH BUILDER ===

def create_moderation_graph():
    """Build the moderation pipeline.
    
    Visual flow:
    safety → (pass) → topic → (pass) → quality → approve/reject
              ↓                ↓                      
           reject           reject
    """
    graph = StateGraph(ModerationState)
    
    # Add all nodes
    graph.add_node("check_safety", check_safety)
    graph.add_node("check_topic", check_topic)
    graph.add_node("check_quality", check_quality)
    graph.add_node("approve", approve)
    graph.add_node("approve_with_note", approve_with_note)
    graph.add_node("reject_unsafe", reject_unsafe)
    graph.add_node("reject_off_topic", reject_off_topic)
    graph.add_node("reject_low_quality", reject_low_quality)
    
    # Start with safety
    graph.set_entry_point("check_safety")
    
    # Chain the decisions - each gate leads to the next or to rejection
    graph.add_conditional_edges(
        "check_safety",
        route_after_safety,
        {"check_topic": "check_topic", "reject_unsafe": "reject_unsafe"}
    )
    
    graph.add_conditional_edges(
        "check_topic",
        route_after_topic,
        {"check_quality": "check_quality", "reject_off_topic": "reject_off_topic"}
    )
    
    graph.add_conditional_edges(
        "check_quality",
        route_after_quality,
        {
            "approve": "approve",
            "approve_with_note": "approve_with_note",
            "reject_low_quality": "reject_low_quality"
        }
    )
    
    # All terminal nodes go to END
    for node in ["approve", "approve_with_note", "reject_unsafe", 
                 "reject_off_topic", "reject_low_quality"]:
        graph.add_edge(node, END)
    
    return graph.compile()


# === MAIN ===

def main():
    """Test the moderation pipeline with various content."""
    app = create_moderation_graph()
    
    test_posts = [
        "Here's my detailed guide on setting up Docker containers for Python development...",
        "Check out this awesome new JavaScript framework I found!",
        "HATE HATE HATE everyone who uses tabs instead of spaces!!!",
        "Anyone want to buy cheap watches? Click here: scam.com",
        "hi",
        "What's your favorite recipe for chocolate chip cookies?",
    ]
    
    print("=" * 60)
    print("🔍 Content Moderation Pipeline")
    print("=" * 60)
    
    for post in test_posts:
        print(f"\n📝 Post: {post[:50]}...")
        print("-" * 40)
        
        result = app.invoke({
            "content": post,
            "is_safe": False,
            "is_on_topic": False,
            "quality_score": 0,
            "decision": "",
            "reason": ""
        })
        
        print(f"📋 Decision: {result['decision']}")
        print(f"📋 Reason: {result['reason']}")


if __name__ == "__main__":
    main()
