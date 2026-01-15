# From: Zero to AI Agent, Chapter 17, Section 17.6
# Save as: multi_aspect_feedback.py

from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
evaluator = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

class MultiAspectState(TypedDict):
    task: str
    content: str
    # Aspect scores (1-10)
    style_score: int
    accuracy_score: int
    structure_score: int
    # Feedback per aspect
    style_feedback: str
    accuracy_feedback: str
    structure_feedback: str
    # Control
    iteration: int
    max_iterations: int
    all_pass: bool
    threshold: int

def evaluate_style(state: MultiAspectState) -> dict:
    """Evaluate writing style."""
    prompt = f"""Score the STYLE of this content (1-10).
Consider: tone, readability, engagement, word choice.

Content:
{state['content']}

Return format:
Score: <number>
Feedback: <brief feedback>"""
    
    response = evaluator.invoke(prompt)
    content = response.content
    
    # Parse score
    score = 5
    try:
        score_line = [l for l in content.split('\n') if 'Score' in l][0]
        score = int(''.join(filter(str.isdigit, score_line)))
    except:
        pass
    
    return {
        "style_score": min(10, max(1, score)),
        "style_feedback": content
    }

def evaluate_accuracy(state: MultiAspectState) -> dict:
    """Evaluate factual accuracy."""
    prompt = f"""Score the ACCURACY of this content (1-10).
Consider: factual correctness, precision, reliability.

Content:
{state['content']}

Return format:
Score: <number>
Feedback: <brief feedback>"""
    
    response = evaluator.invoke(prompt)
    content = response.content
    
    score = 5
    try:
        score_line = [l for l in content.split('\n') if 'Score' in l][0]
        score = int(''.join(filter(str.isdigit, score_line)))
    except:
        pass
    
    return {
        "accuracy_score": min(10, max(1, score)),
        "accuracy_feedback": content
    }

def evaluate_structure(state: MultiAspectState) -> dict:
    """Evaluate content structure."""
    prompt = f"""Score the STRUCTURE of this content (1-10).
Consider: organization, flow, completeness, logical order.

Content:
{state['content']}

Return format:
Score: <number>
Feedback: <brief feedback>"""
    
    response = evaluator.invoke(prompt)
    content = response.content
    
    score = 5
    try:
        score_line = [l for l in content.split('\n') if 'Score' in l][0]
        score = int(''.join(filter(str.isdigit, score_line)))
    except:
        pass
    
    return {
        "structure_score": min(10, max(1, score)),
        "structure_feedback": content
    }

def aggregate_and_decide(state: MultiAspectState) -> dict:
    """Aggregate scores and decide if all pass threshold."""
    scores = [
        state["style_score"],
        state["accuracy_score"],
        state["structure_score"]
    ]
    
    all_pass = all(s >= state["threshold"] for s in scores)
    
    return {
        "all_pass": all_pass,
        "iteration": state["iteration"] + 1
    }

def improve_content(state: MultiAspectState) -> dict:
    """Improve content based on all feedback."""
    
    # Find lowest scoring aspect
    scores = {
        "style": (state["style_score"], state["style_feedback"]),
        "accuracy": (state["accuracy_score"], state["accuracy_feedback"]),
        "structure": (state["structure_score"], state["structure_feedback"])
    }
    
    weakest = min(scores.items(), key=lambda x: x[1][0])
    
    prompt = f"""Improve this content, focusing especially on {weakest[0]}.

Task: {state['task']}

Current content:
{state['content']}

Feedback to address:
- Style ({state['style_score']}/10): {state['style_feedback'][:100]}
- Accuracy ({state['accuracy_score']}/10): {state['accuracy_feedback'][:100]}
- Structure ({state['structure_score']}/10): {state['structure_feedback'][:100]}

Priority: Improve {weakest[0]} (lowest score: {weakest[1][0]}/10)

Write improved content:"""
    
    response = llm.invoke(prompt)
    return {"content": response.content}

def generate_initial(state: MultiAspectState) -> dict:
    """Generate initial content."""
    response = llm.invoke(f"Complete this task:\n{state['task']}")
    return {"content": response.content}

def check_quality(state: MultiAspectState) -> str:
    if state["all_pass"]:
        return "done"
    if state["iteration"] >= state["max_iterations"]:
        return "done"
    return "improve"

def build_multi_aspect_graph():
    graph = StateGraph(MultiAspectState)
    
    graph.add_node("generate", generate_initial)
    graph.add_node("eval_style", evaluate_style)
    graph.add_node("eval_accuracy", evaluate_accuracy)
    graph.add_node("eval_structure", evaluate_structure)
    graph.add_node("aggregate", aggregate_and_decide)
    graph.add_node("improve", improve_content)
    
    # Initial generation
    graph.add_edge(START, "generate")
    
    # Parallel evaluation
    graph.add_edge("generate", "eval_style")
    graph.add_edge("generate", "eval_accuracy")
    graph.add_edge("generate", "eval_structure")
    
    # All evaluations feed into aggregate
    graph.add_edge("eval_style", "aggregate")
    graph.add_edge("eval_accuracy", "aggregate")
    graph.add_edge("eval_structure", "aggregate")
    
    # Conditional improvement loop
    graph.add_conditional_edges(
        "aggregate",
        check_quality,
        {
            "improve": "improve",
            "done": END
        }
    )
    
    # After improvement, re-evaluate
    graph.add_edge("improve", "eval_style")
    graph.add_edge("improve", "eval_accuracy")
    graph.add_edge("improve", "eval_structure")
    
    return graph.compile()

def test_multi_aspect():
    graph = build_multi_aspect_graph()
    
    result = graph.invoke({
        "task": "Write a brief guide on effective time management for students",
        "content": "",
        "style_score": 0,
        "accuracy_score": 0,
        "structure_score": 0,
        "style_feedback": "",
        "accuracy_feedback": "",
        "structure_feedback": "",
        "iteration": 0,
        "max_iterations": 3,
        "all_pass": False,
        "threshold": 7
    })
    
    print("📊 Multi-Aspect Feedback Results")
    print("=" * 60)
    print(f"Iterations: {result['iteration']}")
    print(f"All aspects ≥ {result['threshold']}? {'Yes ✅' if result['all_pass'] else 'No'}")
    
    print("\n📈 Final Scores:")
    print(f"  Style: {result['style_score']}/10")
    print(f"  Accuracy: {result['accuracy_score']}/10")
    print(f"  Structure: {result['structure_score']}/10")
    
    print(f"\n📝 Final Content:\n{result['content'][:500]}...")

if __name__ == "__main__":
    test_multi_aspect()
