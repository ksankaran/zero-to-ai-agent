# From: Zero to AI Agent, Chapter 17, Section 17.6
# Save as: reflexion_agent.py

from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
validator_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

class ReflexionState(TypedDict):
    question: str
    current_answer: str
    # External validation
    fact_checks: list[dict]
    # Self-reflection
    reflection: str
    missing_info: list[str]
    # Control
    is_satisfactory: bool
    iteration: int
    max_iterations: int
    revision_history: Annotated[list[str], operator.add]

def generate_answer(state: ReflexionState) -> dict:
    """Generate or revise answer."""
    
    if state["iteration"] == 0:
        prompt = f"Answer this question thoroughly:\n{state['question']}"
    else:
        prompt = f"""Revise your answer based on reflection and fact checks.

Question: {state['question']}

Previous answer:
{state['current_answer']}

Reflection:
{state['reflection']}

Missing information to address:
{', '.join(state['missing_info']) if state['missing_info'] else 'None identified'}

Write an improved, more accurate answer:"""
    
    response = llm.invoke(prompt)
    
    return {
        "current_answer": response.content,
        "revision_history": [f"Revision {state['iteration'] + 1}"]
    }

def validate_claims(state: ReflexionState) -> dict:
    """Extract and validate claims in the answer."""
    
    validation_prompt = f"""Analyze this answer for factual claims.

Question: {state['question']}

Answer:
{state['current_answer']}

For each major claim, assess if it appears accurate.
Return a brief assessment of overall factual reliability (HIGH, MEDIUM, or LOW)
and list any claims that seem questionable or need verification.

Format:
Reliability: <HIGH/MEDIUM/LOW>
Questionable claims: <list or "None">
Missing important information: <list or "None">"""

    response = validator_llm.invoke(validation_prompt)
    content = response.content
    
    # Parse response (simplified)
    reliability = "MEDIUM"
    if "Reliability: HIGH" in content:
        reliability = "HIGH"
    elif "Reliability: LOW" in content:
        reliability = "LOW"
    
    # Extract missing info
    missing = []
    if "Missing" in content:
        missing_section = content.split("Missing")[1].split("\n")[0]
        if "None" not in missing_section:
            missing = [m.strip() for m in missing_section.split(",") if m.strip()]
    
    return {
        "fact_checks": [{"reliability": reliability, "details": content}],
        "missing_info": missing[:3]  # Limit to top 3
    }

def reflect_on_answer(state: ReflexionState) -> dict:
    """Reflect on the answer quality."""
    
    reflection_prompt = f"""Critically evaluate this answer.

Question: {state['question']}

Answer:
{state['current_answer']}

Validation feedback:
{state['fact_checks'][-1]['details'] if state['fact_checks'] else 'No validation yet'}

Reflect on:
1. Is the answer complete and accurate?
2. What could be improved?
3. Are there any gaps or weaknesses?

Provide honest self-reflection:"""

    response = validator_llm.invoke(reflection_prompt)
    
    # Determine if satisfactory
    reflection = response.content.lower()
    is_good = (
        state["fact_checks"] and 
        state["fact_checks"][-1]["reliability"] == "HIGH" and
        "complete" in reflection and
        "no major" in reflection
    )
    
    return {
        "reflection": response.content,
        "is_satisfactory": is_good,
        "iteration": state["iteration"] + 1
    }

def should_revise(state: ReflexionState) -> str:
    """Decide whether to revise or finish."""
    
    if state["is_satisfactory"]:
        return "done"
    
    if state["iteration"] >= state["max_iterations"]:
        return "done"
    
    return "revise"

def build_reflexion_graph():
    graph = StateGraph(ReflexionState)
    
    graph.add_node("generate", generate_answer)
    graph.add_node("validate", validate_claims)
    graph.add_node("reflect", reflect_on_answer)
    
    graph.add_edge(START, "generate")
    graph.add_edge("generate", "validate")
    graph.add_edge("validate", "reflect")
    
    graph.add_conditional_edges(
        "reflect",
        should_revise,
        {
            "revise": "generate",
            "done": END
        }
    )
    
    return graph.compile()

def test_reflexion():
    graph = build_reflexion_graph()
    
    result = graph.invoke({
        "question": "What are the main causes and effects of deforestation?",
        "current_answer": "",
        "fact_checks": [],
        "reflection": "",
        "missing_info": [],
        "is_satisfactory": False,
        "iteration": 0,
        "max_iterations": 3,
        "revision_history": []
    })
    
    print("🔍 Reflexion Agent Results")
    print("=" * 60)
    print(f"Iterations: {result['iteration']}")
    print(f"Satisfactory: {'Yes' if result['is_satisfactory'] else 'No'}")
    
    print("\n📊 Final Validation:")
    if result["fact_checks"]:
        print(f"  Reliability: {result['fact_checks'][-1]['reliability']}")
    
    print(f"\n📝 Final Answer:\n{result['current_answer']}")

if __name__ == "__main__":
    test_reflexion()
