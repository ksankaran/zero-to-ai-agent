# From: Zero to AI Agent, Chapter 16, Section 16.5
# File: exercise_1_16_5_solution.py

"""
Exercise 1 Solution: Add a Fact-Checker

Research team with fact-checking step that assigns confidence levels to findings.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)


class ResearchState(TypedDict):
    topic: str
    questions: list[str]
    findings: list[str]
    checked_findings: list[str]  # New: findings with confidence
    insights: str
    report: str


def planner(state: ResearchState) -> dict:
    """Creates research questions from topic."""
    prompt = f"Create 3 research questions for: {state['topic']}"
    response = llm.invoke(prompt)
    questions = [line.strip()[3:] for line in response.content.split('\n') 
                 if line.strip() and line.strip()[0].isdigit()][:3]
    print(f"📋 Planner: {len(questions)} questions")
    return {"questions": questions}


def researcher(state: ResearchState) -> dict:
    """Gathers findings for each question."""
    findings = []
    for i, q in enumerate(state['questions'], 1):
        response = llm.invoke(f"Answer with 2-3 facts: {q}")
        findings.append(f"Q: {q}\nA: {response.content}")
        print(f"🔍 Researcher: question {i} done")
    return {"findings": findings}


def fact_checker(state: ResearchState) -> dict:
    """
    Reviews findings for plausibility and assigns confidence levels.
    """
    checked = []
    
    for finding in state['findings']:
        prompt = f"""Evaluate this research finding for plausibility:

{finding}

Consider:
- Does this sound factually accurate?
- Is this claim verifiable?
- Are there any red flags?

Respond with:
CONFIDENCE: [HIGH/MEDIUM/LOW]
REASON: [brief explanation]
FINDING: [original finding, possibly with caveats added]"""

        response = llm.invoke(prompt)
        
        # Parse confidence level
        content = response.content
        if "HIGH" in content.upper():
            confidence = "HIGH"
        elif "LOW" in content.upper():
            confidence = "LOW"
        else:
            confidence = "MEDIUM"
        
        checked.append(f"[{confidence} confidence]\n{finding}")
        print(f"🔎 Fact-checker: {confidence} confidence")
    
    return {"checked_findings": checked}


def analyst_weighted(state: ResearchState) -> dict:
    """
    Analyzes findings, giving more weight to high-confidence items.
    """
    all_findings = "\n\n".join(state['checked_findings'])
    
    prompt = f"""Analyze these research findings:

{all_findings}

Note: Findings are marked with confidence levels (HIGH/MEDIUM/LOW).
- Give more weight to HIGH confidence findings
- Be cautious about LOW confidence findings
- Note any areas where confidence is uncertain

Provide 3 key insights based on this weighted analysis."""

    response = llm.invoke(prompt)
    print("🔬 Analyst: weighted analysis complete")
    
    return {"insights": response.content}


def writer(state: ResearchState) -> dict:
    """Writes the final report."""
    prompt = f"""Write a report on: {state['topic']}

INSIGHTS (based on fact-checked findings):
{state['insights']}

Note any areas where findings had lower confidence."""
    
    response = llm.invoke(prompt)
    print("✍️ Writer: report complete")
    return {"report": response.content}


# Build workflow with fact-checker
workflow = StateGraph(ResearchState)

workflow.add_node("planner", planner)
workflow.add_node("researcher", researcher)
workflow.add_node("fact_checker", fact_checker)  # New step
workflow.add_node("analyst", analyst_weighted)
workflow.add_node("writer", writer)

workflow.add_edge(START, "planner")
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "fact_checker")  # Goes through fact-checker
workflow.add_edge("fact_checker", "analyst")
workflow.add_edge("analyst", "writer")
workflow.add_edge("writer", END)

research_team = workflow.compile()


# Test
if __name__ == "__main__":
    result = research_team.invoke({
        "topic": "Effects of coffee consumption on health",
        "questions": [],
        "findings": [],
        "checked_findings": [],
        "insights": "",
        "report": ""
    })
    
    print("\n" + "=" * 60)
    print("FINAL REPORT (with fact-checking)")
    print("=" * 60)
    print(result["report"])
