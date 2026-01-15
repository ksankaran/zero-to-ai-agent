# From: Zero to AI Agent, Chapter 16, Section 16.3
# File: exercise_3_16_3_solution.py

"""
Exercise 3 Solution: Quality Control Supervisor

Quality control supervisor with critic and improvement loops.
"""

from typing import TypedDict, Literal, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import operator
import re

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


class QualityState(TypedDict):
    topic: str
    current_draft: str
    score: int
    feedback: str
    score_history: Annotated[list[int], operator.add]
    improvement_rounds: int
    max_rounds: int
    final_content: str


def writer(state: QualityState) -> dict:
    """Creates initial content."""
    prompt = f"""Write a short, engaging paragraph about:
    {state['topic']}
    
    Make it informative and interesting. About 3-4 sentences."""
    
    response = llm.invoke(prompt)
    print("✍️ Writer created draft")
    
    return {"current_draft": response.content}


def critic(state: QualityState) -> dict:
    """Scores content and provides feedback."""
    prompt = f"""Rate this content from 1-10 and provide brief feedback:
    
    {state['current_draft']}
    
    Criteria:
    - Clarity (is it easy to understand?)
    - Engagement (is it interesting?)
    - Accuracy (does it seem factual?)
    
    Format:
    SCORE: [number]
    FEEDBACK: [your feedback]"""
    
    response = llm.invoke(prompt)
    
    # Parse score
    score_match = re.search(r'SCORE:\s*(\d+)', response.content)
    score = int(score_match.group(1)) if score_match else 5
    
    # Parse feedback
    feedback_match = re.search(r'FEEDBACK:\s*(.+)', response.content, re.DOTALL)
    feedback = feedback_match.group(1).strip() if feedback_match else response.content
    
    print(f"🎯 Critic scored: {score}/10")
    
    return {
        "score": score,
        "feedback": feedback,
        "score_history": [score]
    }


def improver(state: QualityState) -> dict:
    """Revises content based on feedback."""
    rounds = state.get("improvement_rounds", 0) + 1
    
    prompt = f"""Improve this content based on the feedback:
    
    CURRENT DRAFT:
    {state['current_draft']}
    
    FEEDBACK:
    {state['feedback']}
    
    Write an improved version addressing the feedback.
    Keep it about the same length."""
    
    response = llm.invoke(prompt)
    print(f"📝 Improver completed round {rounds}")
    
    return {
        "current_draft": response.content,
        "improvement_rounds": rounds
    }


def quality_supervisor(state: QualityState) -> dict:
    """Decides whether quality is sufficient."""
    score = state.get("score", 0)
    rounds = state.get("improvement_rounds", 0)
    max_rounds = state.get("max_rounds", 3)
    
    if score >= 7:
        print(f"✅ Supervisor: Quality achieved! (score: {score})")
    elif rounds >= max_rounds:
        print(f"⚠️ Supervisor: Max rounds reached (score: {score})")
    else:
        print(f"🔄 Supervisor: Needs improvement (score: {score}, round {rounds + 1})")
    
    return {}


def should_improve(state: QualityState) -> Literal["improve", "finalize"]:
    """Decides whether to improve or finalize."""
    score = state.get("score", 0)
    rounds = state.get("improvement_rounds", 0)
    max_rounds = state.get("max_rounds", 3)
    
    if score >= 7 or rounds >= max_rounds:
        return "finalize"
    return "improve"


def finalizer(state: QualityState) -> dict:
    """Packages final content with quality report."""
    history = state.get("score_history", [])
    
    final = f"""
FINAL CONTENT
{'='*40}
{state['current_draft']}

{'='*40}
QUALITY REPORT
- Final Score: {state['score']}/10
- Improvement Rounds: {state['improvement_rounds']}
- Score History: {' → '.join(map(str, history))}
"""
    return {"final_content": final}


# Build the workflow
workflow = StateGraph(QualityState)

workflow.add_node("writer", writer)
workflow.add_node("critic", critic)
workflow.add_node("supervisor", quality_supervisor)
workflow.add_node("improver", improver)
workflow.add_node("finalizer", finalizer)

# Start with writer
workflow.add_edge(START, "writer")
workflow.add_edge("writer", "critic")
workflow.add_edge("critic", "supervisor")

# Supervisor decides: improve or finalize
workflow.add_conditional_edges(
    "supervisor",
    should_improve,
    {
        "improve": "improver",
        "finalize": "finalizer"
    }
)

# After improvement, back to critic
workflow.add_edge("improver", "critic")

workflow.add_edge("finalizer", END)

app = workflow.compile()

# Test the quality loop
result = app.invoke({
    "topic": "The importance of sleep for productivity",
    "current_draft": "",
    "score": 0,
    "feedback": "",
    "score_history": [],
    "improvement_rounds": 0,
    "max_rounds": 3,
    "final_content": ""
})

print(result["final_content"])
