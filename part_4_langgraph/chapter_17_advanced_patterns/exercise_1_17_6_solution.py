# From: Zero to AI Agent, Chapter 17, Section 17.6
# Save as: exercise_1_17_6_solution.py
# Exercise 1: Essay Improver

import json
from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
scorer = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

class EssayState(TypedDict):
    essay: str
    # Individual scores
    thesis_clarity: int
    evidence_quality: int
    writing_style: int
    conclusion_strength: int
    # Feedback
    feedback: str
    # Control
    iteration: int
    max_iterations: int
    target_score: int
    score_history: Annotated[list[dict], operator.add]
    all_pass: bool

def score_essay(state: EssayState) -> dict:
    """Score the essay on four dimensions."""
    
    prompt = f"""Score this essay on these criteria (1-10 each):
1. Thesis Clarity - Is the main argument clear and well-stated?
2. Evidence Quality - Are claims supported with good evidence?
3. Writing Style - Is the writing clear, engaging, and grammatically correct?
4. Conclusion Strength - Does the conclusion effectively summarize and close?

Essay:
{state['essay']}

Return ONLY valid JSON:
{{
    "thesis_clarity": <1-10>,
    "evidence_quality": <1-10>,
    "writing_style": <1-10>,
    "conclusion_strength": <1-10>,
    "feedback": "<specific improvement suggestions>"
}}"""
    
    response = scorer.invoke(prompt)
    
    try:
        scores = json.loads(response.content)
        
        all_pass = all([
            scores.get("thesis_clarity", 0) >= state["target_score"],
            scores.get("evidence_quality", 0) >= state["target_score"],
            scores.get("writing_style", 0) >= state["target_score"],
            scores.get("conclusion_strength", 0) >= state["target_score"]
        ])
        
        return {
            "thesis_clarity": scores.get("thesis_clarity", 5),
            "evidence_quality": scores.get("evidence_quality", 5),
            "writing_style": scores.get("writing_style", 5),
            "conclusion_strength": scores.get("conclusion_strength", 5),
            "feedback": scores.get("feedback", ""),
            "all_pass": all_pass,
            "score_history": [{
                "iteration": state["iteration"],
                "thesis": scores.get("thesis_clarity", 5),
                "evidence": scores.get("evidence_quality", 5),
                "style": scores.get("writing_style", 5),
                "conclusion": scores.get("conclusion_strength", 5)
            }]
        }
    except json.JSONDecodeError:
        return {
            "thesis_clarity": 5,
            "evidence_quality": 5,
            "writing_style": 5,
            "conclusion_strength": 5,
            "feedback": "Could not parse scores",
            "all_pass": False,
            "score_history": []
        }

def improve_essay(state: EssayState) -> dict:
    """Improve essay based on feedback."""
    
    # Find weakest area
    scores = {
        "thesis clarity": state["thesis_clarity"],
        "evidence quality": state["evidence_quality"],
        "writing style": state["writing_style"],
        "conclusion strength": state["conclusion_strength"]
    }
    weakest = min(scores.items(), key=lambda x: x[1])
    
    prompt = f"""Improve this essay. Focus especially on: {weakest[0]} (score: {weakest[1]}/10)

Current scores:
- Thesis Clarity: {state['thesis_clarity']}/10
- Evidence Quality: {state['evidence_quality']}/10
- Writing Style: {state['writing_style']}/10
- Conclusion Strength: {state['conclusion_strength']}/10

Feedback to address:
{state['feedback']}

Current Essay:
{state['essay']}

Write the improved essay:"""
    
    response = llm.invoke(prompt)
    
    return {
        "essay": response.content,
        "iteration": state["iteration"] + 1
    }

def check_essay_quality(state: EssayState) -> str:
    """Check if essay meets quality threshold."""
    if state["all_pass"]:
        return "done"
    if state["iteration"] >= state["max_iterations"]:
        return "done"
    return "improve"

def build_essay_improver():
    graph = StateGraph(EssayState)
    
    graph.add_node("score", score_essay)
    graph.add_node("improve", improve_essay)
    
    # Start with scoring the input essay
    graph.add_edge(START, "score")
    
    # After scoring, decide
    graph.add_conditional_edges(
        "score",
        check_essay_quality,
        {
            "improve": "improve",
            "done": END
        }
    )
    
    # After improvement, re-score
    graph.add_edge("improve", "score")
    
    return graph.compile()

def test_essay_improver():
    graph = build_essay_improver()
    
    # Sample rough draft
    rough_draft = """
    Technology is changing education. Many students now use computers and tablets 
    in school. This has both good and bad effects. Some people think technology 
    helps learning. Others think it is distracting. The debate continues.
    
    One benefit is access to information. Students can look things up quickly.
    They can also communicate with teachers easily. This is helpful.
    
    However, there are problems too. Some students get distracted by games
    and social media. This hurts their grades. Teachers also need training.
    
    In conclusion, technology in education is complicated. We need to think
    carefully about how to use it.
    """
    
    result = graph.invoke({
        "essay": rough_draft,
        "thesis_clarity": 0,
        "evidence_quality": 0,
        "writing_style": 0,
        "conclusion_strength": 0,
        "feedback": "",
        "iteration": 0,
        "max_iterations": 4,
        "target_score": 7,
        "score_history": [],
        "all_pass": False
    })
    
    print("📝 Essay Improver Results")
    print("=" * 60)
    print(f"Iterations: {result['iteration']}")
    print(f"All scores ≥ 7? {'Yes ✅' if result['all_pass'] else 'No'}")
    
    print("\n📈 Score Progression:")
    for entry in result["score_history"]:
        print(f"  Iteration {entry['iteration']}: "
              f"Thesis={entry['thesis']}, Evidence={entry['evidence']}, "
              f"Style={entry['style']}, Conclusion={entry['conclusion']}")
    
    print("\n📊 Final Scores:")
    print(f"  Thesis Clarity: {result['thesis_clarity']}/10")
    print(f"  Evidence Quality: {result['evidence_quality']}/10")
    print(f"  Writing Style: {result['writing_style']}/10")
    print(f"  Conclusion Strength: {result['conclusion_strength']}/10")
    
    print(f"\n📝 Final Essay:\n{result['essay']}")

if __name__ == "__main__":
    test_essay_improver()
