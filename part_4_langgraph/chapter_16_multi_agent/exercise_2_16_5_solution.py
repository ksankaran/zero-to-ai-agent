# From: Zero to AI Agent, Chapter 16, Section 16.5
# File: exercise_2_16_5_solution.py

"""
Exercise 2 Solution: Parallel Research

Research team with parallel perspective gathering:
- Academic perspective (research and studies)
- Practical perspective (real-world applications)
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)


class ParallelResearchState(TypedDict):
    topic: str
    questions: list[str]
    academic_findings: list[str]
    practical_findings: list[str]
    combined_insights: str
    report: str


def planner(state: ParallelResearchState) -> dict:
    """Creates research questions from topic."""
    prompt = f"Create 3 research questions for: {state['topic']}"
    response = llm.invoke(prompt)
    questions = [line.strip()[3:] for line in response.content.split('\n') 
                 if line.strip() and line.strip()[0].isdigit()][:3]
    print(f"📋 Planner: {len(questions)} questions")
    return {"questions": questions}


def academic_researcher(state: ParallelResearchState) -> dict:
    """
    Researches from an academic/scientific perspective.
    """
    findings = []
    
    for q in state['questions']:
        prompt = f"""Answer this question from an ACADEMIC perspective:

{q}

Focus on:
- Scientific studies and research
- Peer-reviewed findings
- Statistical evidence

Keep response to 2-3 sentences."""

        response = llm.invoke(prompt)
        findings.append(f"[Academic] {q}\n{response.content}")
    
    print(f"📚 Academic researcher: {len(findings)} findings")
    return {"academic_findings": findings}


def practical_researcher(state: ParallelResearchState) -> dict:
    """
    Researches from a practical/applied perspective.
    """
    findings = []
    
    for q in state['questions']:
        prompt = f"""Answer this question from a PRACTICAL perspective:

{q}

Focus on:
- Real-world applications
- Industry examples
- Practical implications

Keep response to 2-3 sentences."""

        response = llm.invoke(prompt)
        findings.append(f"[Practical] {q}\n{response.content}")
    
    print(f"🔧 Practical researcher: {len(findings)} findings")
    return {"practical_findings": findings}


def synthesizing_analyst(state: ParallelResearchState) -> dict:
    """
    Combines academic and practical perspectives.
    """
    academic = "\n\n".join(state['academic_findings'])
    practical = "\n\n".join(state['practical_findings'])
    
    prompt = f"""Synthesize these two research perspectives:

ACADEMIC PERSPECTIVE:
{academic}

PRACTICAL PERSPECTIVE:
{practical}

Provide:
1. Where do academic and practical findings AGREE?
2. Where do they DIFFER or offer different insights?
3. What's the COMPLETE picture when both are considered?

Give 3-4 key synthesized insights."""

    response = llm.invoke(prompt)
    print("🔬 Analyst: perspectives synthesized")
    
    return {"combined_insights": response.content}


def writer(state: ParallelResearchState) -> dict:
    """Writes the final balanced report."""
    prompt = f"""Write a balanced report on: {state['topic']}

SYNTHESIZED INSIGHTS (combining academic and practical views):
{state['combined_insights']}

Present both the research evidence and real-world applications."""

    response = llm.invoke(prompt)
    print("✍️ Writer: report complete")
    return {"report": response.content}


# Build with parallel research
workflow = StateGraph(ParallelResearchState)

workflow.add_node("planner", planner)
workflow.add_node("academic", academic_researcher)
workflow.add_node("practical", practical_researcher)
workflow.add_node("analyst", synthesizing_analyst)
workflow.add_node("writer", writer)

workflow.add_edge(START, "planner")

# Parallel: both researchers start after planner
workflow.add_edge("planner", "academic")
workflow.add_edge("planner", "practical")

# Both feed into analyst
workflow.add_edge("academic", "analyst")
workflow.add_edge("practical", "analyst")

workflow.add_edge("analyst", "writer")
workflow.add_edge("writer", END)

research_team = workflow.compile()


# Test
if __name__ == "__main__":
    result = research_team.invoke({
        "topic": "Remote work productivity",
        "questions": [],
        "academic_findings": [],
        "practical_findings": [],
        "combined_insights": "",
        "report": ""
    })
    
    print("\n" + "=" * 60)
    print("FINAL REPORT (dual perspective)")
    print("=" * 60)
    print(result["report"])
