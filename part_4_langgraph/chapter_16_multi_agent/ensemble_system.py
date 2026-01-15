# From: Zero to AI Agent, Chapter 16, Section 16.4
# File: ensemble_system.py

"""
Ensemble pattern: Multiple agents solve independently, then merge.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.8)  # Higher temp for diversity


class EnsembleState(TypedDict):
    problem: str
    solution_creative: str
    solution_analytical: str
    solution_practical: str
    merged_solution: str


def creative_solver(state: EnsembleState) -> dict:
    """Approaches problem creatively."""
    prompt = f"""Solve this problem with CREATIVE thinking:
    
    {state['problem']}
    
    Think outside the box. Consider unconventional approaches.
    Be imaginative but still address the core problem."""
    
    response = llm.invoke(prompt)
    print("🎨 Creative solver complete")
    return {"solution_creative": response.content}


def analytical_solver(state: EnsembleState) -> dict:
    """Approaches problem analytically."""
    prompt = f"""Solve this problem with ANALYTICAL thinking:
    
    {state['problem']}
    
    Break it down systematically. Consider data and logic.
    Be thorough and evidence-based."""
    
    response = llm.invoke(prompt)
    print("📊 Analytical solver complete")
    return {"solution_analytical": response.content}


def practical_solver(state: EnsembleState) -> dict:
    """Approaches problem practically."""
    prompt = f"""Solve this problem with PRACTICAL thinking:
    
    {state['problem']}
    
    Focus on what's actionable and realistic.
    Consider constraints and implementation."""
    
    response = llm.invoke(prompt)
    print("🔧 Practical solver complete")
    return {"solution_practical": response.content}


def solution_merger(state: EnsembleState) -> dict:
    """Synthesizes the three approaches into one solution."""
    prompt = f"""Synthesize these three approaches to the problem:
    
    PROBLEM: {state['problem']}
    
    CREATIVE APPROACH:
    {state['solution_creative']}
    
    ANALYTICAL APPROACH:
    {state['solution_analytical']}
    
    PRACTICAL APPROACH:
    {state['solution_practical']}
    
    Create a unified solution that:
    1. Takes the best ideas from each approach
    2. Resolves any contradictions
    3. Is both innovative AND actionable
    
    Provide a clear, integrated recommendation."""
    
    response = llm.invoke(prompt)
    print("🔀 Solutions merged")
    return {"merged_solution": response.content}


# Build with parallel execution
workflow = StateGraph(EnsembleState)

workflow.add_node("creative", creative_solver)
workflow.add_node("analytical", analytical_solver)
workflow.add_node("practical", practical_solver)
workflow.add_node("merger", solution_merger)

# All three solvers start in parallel
workflow.add_edge(START, "creative")
workflow.add_edge(START, "analytical")
workflow.add_edge(START, "practical")

# All feed into merger
workflow.add_edge("creative", "merger")
workflow.add_edge("analytical", "merger")
workflow.add_edge("practical", "merger")

workflow.add_edge("merger", END)

app = workflow.compile()

# Test ensemble solving
result = app.invoke({
    "problem": """Our startup needs to acquire our first 1000 customers 
    with a limited budget of $5000. We're a B2B SaaS tool for project management.""",
    "solution_creative": "",
    "solution_analytical": "",
    "solution_practical": "",
    "merged_solution": ""
})

print("\n" + "=" * 60)
print("ENSEMBLE SOLUTION")
print("=" * 60)
print(result["merged_solution"])
