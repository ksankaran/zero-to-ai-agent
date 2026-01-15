# From: Zero to AI Agent, Chapter 16, Section 16.5
# File: research_team_complete.py

"""
Complete multi-agent research assistant team.
Combines sequential pipeline with quality review loop.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)


# === STATE ===

class ResearchState(TypedDict):
    topic: str
    questions: list[str]
    findings: list[str]
    insights: str
    report: str
    feedback: str
    revision_count: int
    approved: bool


# === AGENTS ===

def planner(state: ResearchState) -> dict:
    """Creates research questions from topic."""
    prompt = f"""Create 3 research questions for: {state['topic']}
    
Format: numbered list, one question per line."""
    
    response = llm.invoke(prompt)
    questions = [line.strip()[3:] for line in response.content.split('\n') 
                 if line.strip() and line.strip()[0].isdigit()][:3]
    
    print(f"📋 Planner: {len(questions)} questions created")
    return {"questions": questions}


def researcher(state: ResearchState) -> dict:
    """Gathers findings for each question."""
    findings = []
    for i, q in enumerate(state['questions'], 1):
        prompt = f"Answer briefly with 2-3 facts: {q}"
        response = llm.invoke(prompt)
        findings.append(f"Q: {q}\nA: {response.content}")
        print(f"🔍 Researcher: question {i} done")
    return {"findings": findings}


def analyst(state: ResearchState) -> dict:
    """Extracts insights from findings."""
    prompt = f"""Analyze these findings and give 3 key insights:
    
{chr(10).join(state['findings'])}"""
    
    response = llm.invoke(prompt)
    print("🔬 Analyst: insights extracted")
    return {"insights": response.content}


def writer(state: ResearchState) -> dict:
    """Writes or revises the report."""
    if state.get('feedback'):
        prompt = f"""Revise this report based on feedback:
        
REPORT: {state['report']}

FEEDBACK: {state['feedback']}"""
    else:
        prompt = f"""Write a short report on: {state['topic']}

INSIGHTS: {state['insights']}

Include intro, findings, conclusion."""
    
    response = llm.invoke(prompt)
    action = "revised" if state.get('feedback') else "written"
    print(f"✍️ Writer: report {action}")
    return {"report": response.content, "revision_count": state.get('revision_count', 0) + 1}


def reviewer(state: ResearchState) -> dict:
    """Reviews report quality."""
    prompt = f"""Review this report. Reply APPROVED if good, or REVISE: [feedback] if not.

{state['report']}"""
    
    response = llm.invoke(prompt)
    approved = "APPROVED" in response.content.upper()
    print(f"{'✅ Approved' if approved else '📝 Needs revision'}")
    
    return {
        "approved": approved,
        "feedback": "" if approved else response.content
    }


def should_continue(state: ResearchState) -> Literal["revise", "done"]:
    """Check if we should revise or finish."""
    if state.get("approved") or state.get("revision_count", 0) >= 2:
        return "done"
    return "revise"


# === BUILD GRAPH ===

workflow = StateGraph(ResearchState)

workflow.add_node("planner", planner)
workflow.add_node("researcher", researcher)
workflow.add_node("analyst", analyst)
workflow.add_node("writer", writer)
workflow.add_node("reviewer", reviewer)

workflow.add_edge(START, "planner")
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "writer")
workflow.add_edge("writer", "reviewer")

workflow.add_conditional_edges("reviewer", should_continue, {
    "revise": "writer",
    "done": END
})

research_team = workflow.compile()


# === RUN ===

if __name__ == "__main__":
    result = research_team.invoke({
        "topic": "Benefits of meditation for stress reduction",
        "questions": [],
        "findings": [],
        "insights": "",
        "report": "",
        "feedback": "",
        "revision_count": 0,
        "approved": False
    })
    
    print("\n" + "=" * 60)
    print("FINAL REPORT")
    print("=" * 60)
    print(result["report"])
