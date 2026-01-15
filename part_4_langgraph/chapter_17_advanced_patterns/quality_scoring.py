# From: Zero to AI Agent, Chapter 17, Section 17.6
# Save as: quality_scoring.py

import json
from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
scorer_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

class ScoredState(TypedDict):
    task: str
    current_output: str
    scores: dict  # {"clarity": 8, "accuracy": 7, ...}
    overall_score: float
    feedback: str
    iteration: int
    max_iterations: int
    target_score: float
    score_history: Annotated[list[dict], operator.add]

def score_output(state: ScoredState) -> dict:
    """Score the output on multiple dimensions."""
    
    scoring_prompt = f"""Score this output on a scale of 1-10 for each criterion.

Task: {state['task']}

Output:
{state['current_output']}

Score each criterion and provide brief feedback.
Return as JSON:
{{
    "clarity": <1-10>,
    "accuracy": <1-10>,
    "completeness": <1-10>,
    "engagement": <1-10>,
    "feedback": "<specific suggestions for improvement>"
}}

Return ONLY valid JSON:"""

    response = scorer_llm.invoke(scoring_prompt)
    
    try:
        scores = json.loads(response.content)
        
        # Calculate overall score
        score_values = [
            scores.get("clarity", 5),
            scores.get("accuracy", 5),
            scores.get("completeness", 5),
            scores.get("engagement", 5)
        ]
        overall = sum(score_values) / len(score_values)
        
        return {
            "scores": scores,
            "overall_score": overall,
            "feedback": scores.get("feedback", ""),
            "score_history": [{
                "iteration": state["iteration"],
                "overall": overall,
                "scores": scores
            }]
        }
    except json.JSONDecodeError:
        # Fallback if parsing fails
        return {
            "scores": {},
            "overall_score": 5.0,
            "feedback": "Could not parse scores",
            "score_history": []
        }

def generate_output(state: ScoredState) -> dict:
    """Generate or improve output."""
    
    if state["iteration"] == 0:
        prompt = f"Complete this task:\n{state['task']}"
    else:
        prompt = f"""Improve this output based on feedback.

Task: {state['task']}

Current output:
{state['current_output']}

Feedback (current score: {state['overall_score']:.1f}/10):
{state['feedback']}

Write an improved version that addresses the feedback:"""
    
    response = llm.invoke(prompt)
    
    return {
        "current_output": response.content,
        "iteration": state["iteration"] + 1
    }

def check_quality(state: ScoredState) -> str:
    """Check if quality threshold is met."""
    
    # Stop if target score reached
    if state["overall_score"] >= state["target_score"]:
        return "done"
    
    # Stop if max iterations reached
    if state["iteration"] >= state["max_iterations"]:
        return "done"
    
    return "improve"

def build_scoring_graph():
    graph = StateGraph(ScoredState)
    
    graph.add_node("generate", generate_output)
    graph.add_node("score", score_output)
    
    graph.add_edge(START, "generate")
    graph.add_edge("generate", "score")
    
    graph.add_conditional_edges(
        "score",
        check_quality,
        {
            "improve": "generate",
            "done": END
        }
    )
    
    return graph.compile()

def test_quality_scoring():
    graph = build_scoring_graph()
    
    result = graph.invoke({
        "task": "Write a compelling product description for a smart water bottle that tracks hydration",
        "current_output": "",
        "scores": {},
        "overall_score": 0.0,
        "feedback": "",
        "iteration": 0,
        "max_iterations": 4,
        "target_score": 8.0,
        "score_history": []
    })
    
    print("📊 Quality Scoring Results")
    print("=" * 60)
    print(f"Final Score: {result['overall_score']:.1f}/10")
    print(f"Target Score: {result['target_score']}/10")
    print(f"Iterations: {result['iteration']}")
    
    print("\n📈 Score History:")
    for entry in result["score_history"]:
        print(f"  Iteration {entry['iteration']}: {entry['overall']:.1f}/10")
    
    print(f"\n📝 Final Output:\n{result['current_output']}")

if __name__ == "__main__":
    test_quality_scoring()
