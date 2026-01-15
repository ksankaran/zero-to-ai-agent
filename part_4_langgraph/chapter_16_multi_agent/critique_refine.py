# From: Zero to AI Agent, Chapter 16, Section 16.4
# File: critique_refine.py

"""
Collaborative critique and refinement between agents.
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import operator

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


class CritiqueState(TypedDict):
    task: str
    current_work: str
    critique_history: Annotated[list[str], operator.add]
    revision_count: int
    max_revisions: int
    is_approved: bool
    final_work: str


def creator(state: CritiqueState) -> dict:
    """Creates or revises the work based on critique."""
    revision = state.get("revision_count", 0)
    critique_history = state.get("critique_history", [])
    current = state.get("current_work", "")
    
    if revision == 0:
        # Initial creation
        prompt = f"""Create a response for this task:
        {state['task']}
        
        Be thorough but concise."""
    else:
        # Revision based on critique
        latest_critique = critique_history[-1] if critique_history else ""
        prompt = f"""Revise your work based on this critique:
        
        TASK: {state['task']}
        
        YOUR PREVIOUS WORK:
        {current}
        
        CRITIQUE:
        {latest_critique}
        
        Address the concerns while keeping what works."""
    
    response = llm.invoke(prompt)
    action = "Created" if revision == 0 else f"Revised (v{revision + 1})"
    print(f"✍️ Creator: {action}")
    
    return {
        "current_work": response.content,
        "revision_count": revision + 1
    }


def critic(state: CritiqueState) -> dict:
    """Evaluates the work and provides constructive critique."""
    prompt = f"""Evaluate this work critically but constructively:
    
    TASK: {state['task']}
    
    WORK TO EVALUATE:
    {state['current_work']}
    
    Provide:
    1. What works well (be specific)
    2. What needs improvement (be specific)  
    3. VERDICT: APPROVE if good enough, or REVISE if needs work
    
    Be fair but maintain high standards."""
    
    response = llm.invoke(prompt)
    
    is_approved = "APPROVE" in response.content.upper() and "REVISE" not in response.content.upper()
    
    verdict = "APPROVED ✓" if is_approved else "NEEDS REVISION"
    print(f"🔍 Critic: {verdict}")
    
    return {
        "critique_history": [response.content],
        "is_approved": is_approved
    }


def should_revise(state: CritiqueState) -> str:
    """Decides whether to revise or finalize."""
    if state.get("is_approved", False):
        return "finalize"
    
    revisions = state.get("revision_count", 0)
    max_rev = state.get("max_revisions", 3)
    
    if revisions >= max_rev:
        print(f"⚠️ Max revisions ({max_rev}) reached")
        return "finalize"
    
    return "revise"


def finalizer(state: CritiqueState) -> dict:
    """Packages the final approved work."""
    return {"final_work": state["current_work"]}


# Build the collaborative workflow
workflow = StateGraph(CritiqueState)

workflow.add_node("creator", creator)
workflow.add_node("critic", critic)
workflow.add_node("finalizer", finalizer)

workflow.add_edge(START, "creator")
workflow.add_edge("creator", "critic")

workflow.add_conditional_edges(
    "critic",
    should_revise,
    {
        "revise": "creator",
        "finalize": "finalizer"
    }
)

workflow.add_edge("finalizer", END)

app = workflow.compile()

# Test the critique cycle
result = app.invoke({
    "task": "Write a professional bio for a software engineer with 5 years experience",
    "current_work": "",
    "critique_history": [],
    "revision_count": 0,
    "max_revisions": 3,
    "is_approved": False,
    "final_work": ""
})

print("\n" + "=" * 60)
print(f"FINAL WORK (after {result['revision_count']} revisions)")
print("=" * 60)
print(result["final_work"])
print("\n" + "=" * 60)
print("CRITIQUE HISTORY")
print("=" * 60)
for i, critique in enumerate(result["critique_history"], 1):
    print(f"\n--- Critique {i} ---")
    print(critique[:200] + "...")
