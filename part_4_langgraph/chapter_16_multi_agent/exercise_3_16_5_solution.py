# From: Zero to AI Agent, Chapter 16, Section 16.5
# File: exercise_3_16_5_solution.py

"""
Exercise 3 Solution: Automatic Gap Detection

Research team with automatic gap detection and follow-up research.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)


class GapDetectionState(TypedDict):
    topic: str
    questions: list[str]
    findings: list[str]
    insights: str
    gaps: list[str]
    additional_findings: list[str]
    has_gaps: bool
    gap_check_done: bool
    report: str


def planner(state: GapDetectionState) -> dict:
    """Creates research questions from topic."""
    prompt = f"Create 3 research questions for: {state['topic']}"
    response = llm.invoke(prompt)
    questions = [line.strip()[3:] for line in response.content.split('\n') 
                 if line.strip() and line.strip()[0].isdigit()][:3]
    print(f"📋 Planner: {len(questions)} questions")
    return {"questions": questions}


def researcher(state: GapDetectionState) -> dict:
    """Gathers findings for each question."""
    findings = []
    for i, q in enumerate(state['questions'], 1):
        response = llm.invoke(f"Answer briefly with 2-3 facts: {q}")
        findings.append(f"Q{i}: {q}\nA: {response.content}")
        print(f"🔍 Researcher: question {i} done")
    return {"findings": findings}


def analyst(state: GapDetectionState) -> dict:
    """Extracts insights from all findings."""
    all_findings = "\n\n".join(state['findings'])
    
    # Include additional findings if we have them
    if state.get('additional_findings'):
        all_findings += "\n\nADDITIONAL RESEARCH:\n"
        all_findings += "\n\n".join(state['additional_findings'])
    
    prompt = f"Give 3 key insights from:\n{all_findings}"
    response = llm.invoke(prompt)
    print("🔬 Analyst: complete")
    return {"insights": response.content}


def gap_detector(state: GapDetectionState) -> dict:
    """
    Reviews findings and identifies areas needing more research.
    """
    all_findings = "\n\n".join(state['findings'])
    questions = "\n".join(state['questions'])
    
    prompt = f"""Review these research findings and identify gaps:

ORIGINAL QUESTIONS:
{questions}

FINDINGS:
{all_findings}

INSIGHTS:
{state['insights']}

Check:
1. Were all questions adequately answered?
2. Are there obvious follow-up questions that should be explored?
3. Are any claims unsupported or vague?

If there are gaps, list up to 2 specific follow-up questions.
If the research is complete, respond with: NO GAPS

Format (if gaps exist):
GAP 1: [specific follow-up question]
GAP 2: [specific follow-up question]"""

    response = llm.invoke(prompt)
    content = response.content.strip()
    
    # Check if gaps were found
    has_gaps = "NO GAPS" not in content.upper() and "GAP" in content.upper()
    
    gaps = []
    if has_gaps:
        for line in content.split('\n'):
            if line.strip().upper().startswith("GAP"):
                # Extract the question after "GAP X:"
                parts = line.split(':', 1)
                if len(parts) > 1:
                    gaps.append(parts[1].strip())
    
    if gaps:
        print(f"🔎 Gap detector: found {len(gaps)} gaps")
        for g in gaps:
            print(f"   - {g[:50]}...")
    else:
        print("✅ Gap detector: research is complete")
    
    return {
        "gaps": gaps,
        "has_gaps": len(gaps) > 0,
        "gap_check_done": True
    }


def followup_researcher(state: GapDetectionState) -> dict:
    """
    Does additional research on identified gaps.
    """
    additional = []
    
    for i, gap in enumerate(state['gaps'], 1):
        prompt = f"""Research this follow-up question:

{gap}

Provide 2-3 specific facts or findings."""

        response = llm.invoke(prompt)
        additional.append(f"Follow-up {i}: {gap}\nFindings: {response.content}")
        print(f"🔍 Follow-up research: gap {i} done")
    
    return {"additional_findings": additional}


def writer(state: GapDetectionState) -> dict:
    """Writes the final comprehensive report."""
    all_findings = "\n\n".join(state['findings'])
    
    if state.get('additional_findings'):
        all_findings += "\n\nADDITIONAL RESEARCH:\n"
        all_findings += "\n\n".join(state['additional_findings'])
    
    prompt = f"""Write a report on: {state['topic']}

FINDINGS:
{all_findings}

INSIGHTS:
{state['insights']}

Include intro, findings, and conclusion."""

    response = llm.invoke(prompt)
    print("✍️ Writer: report complete")
    return {"report": response.content}


def should_do_followup(state: GapDetectionState) -> Literal["followup", "write"]:
    """Check if we need follow-up research."""
    if state.get("has_gaps", False) and not state.get("additional_findings"):
        return "followup"
    return "write"


# Build the workflow
workflow = StateGraph(GapDetectionState)

workflow.add_node("planner", planner)
workflow.add_node("researcher", researcher)
workflow.add_node("analyst", analyst)
workflow.add_node("gap_detector", gap_detector)
workflow.add_node("followup", followup_researcher)
workflow.add_node("writer", writer)

# Main flow
workflow.add_edge(START, "planner")
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "gap_detector")

# Gap detection branching
workflow.add_conditional_edges(
    "gap_detector",
    should_do_followup,
    {
        "followup": "followup",
        "write": "writer"
    }
)

# After follow-up, re-analyze then write
workflow.add_edge("followup", "analyst")

workflow.add_edge("writer", END)

research_team = workflow.compile()


# Test
if __name__ == "__main__":
    result = research_team.invoke({
        "topic": "The impact of social media on mental health",
        "questions": [],
        "findings": [],
        "insights": "",
        "gaps": [],
        "additional_findings": [],
        "has_gaps": False,
        "gap_check_done": False,
        "report": ""
    })
    
    print("\n" + "=" * 60)
    print("FINAL REPORT (with gap detection)")
    print("=" * 60)
    print(result["report"])
