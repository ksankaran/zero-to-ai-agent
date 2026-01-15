# From: Zero to AI Agent, Chapter 16, Section 16.5
# File: research_team_with_review.py

"""
Research team with quality review loop.
Adds a reviewer that can request revisions before final output.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)


class ResearchStateWithReview(TypedDict):
    topic: str
    questions: list[str]
    findings: list[str]
    insights: str
    report: str
    review_feedback: str
    revision_count: int
    max_revisions: int
    approved: bool


def planner_agent(state: ResearchStateWithReview) -> dict:
    """Creates research questions from topic."""
    prompt = f"""You are a research planner. Given a topic, create exactly 3 
focused research questions.

TOPIC: {state['topic']}

Format: numbered list, one question per line."""
    
    response = llm.invoke(prompt)
    lines = response.content.strip().split('\n')
    questions = []
    for line in lines:
        cleaned = line.strip()
        if cleaned and cleaned[0].isdigit():
            cleaned = cleaned[2:].strip() if len(cleaned) > 2 else cleaned
            if cleaned.startswith('.') or cleaned.startswith(')'):
                cleaned = cleaned[1:].strip()
            questions.append(cleaned)
    
    questions = questions[:3]
    print(f"📋 Planner created {len(questions)} research questions")
    return {"questions": questions}


def researcher_agent(state: ResearchStateWithReview) -> dict:
    """Researches each question and gathers findings."""
    findings = []
    
    for i, question in enumerate(state['questions'], 1):
        prompt = f"""Answer this research question with 2-3 key facts:

QUESTION: {question}

Be specific and informative. Keep to 3-4 sentences."""

        response = llm.invoke(prompt)
        finding = f"Q{i}: {question}\nFindings: {response.content}"
        findings.append(finding)
        print(f"🔍 Researched question {i}/{len(state['questions'])}")
    
    return {"findings": findings}


def analyst_agent(state: ResearchStateWithReview) -> dict:
    """Analyzes findings to extract key insights."""
    all_findings = "\n\n".join(state['findings'])
    
    prompt = f"""Analyze these research findings:

TOPIC: {state['topic']}

FINDINGS:
{all_findings}

What are the 2-3 most important takeaways? Be concise but insightful."""

    response = llm.invoke(prompt)
    print("🔬 Analysis complete")
    return {"insights": response.content}


def writer_with_revision(state: ResearchStateWithReview) -> dict:
    """Writes or revises the report based on feedback."""
    all_findings = "\n\n".join(state['findings'])
    
    if state.get('review_feedback'):
        # This is a revision
        prompt = f"""Revise this research report based on feedback:

CURRENT REPORT:
{state['report']}

FEEDBACK:
{state['review_feedback']}

Provide an improved version addressing the feedback."""
    else:
        # Initial write
        prompt = f"""Write a research report on: {state['topic']}

FINDINGS:
{all_findings}

INSIGHTS:
{state['insights']}

Include: introduction, main findings, and conclusion."""

    response = llm.invoke(prompt)
    print("✍️ Report " + ("revised" if state.get('review_feedback') else "written"))
    
    return {"report": response.content}


def reviewer_agent(state: ResearchStateWithReview) -> dict:
    """Reviews the report for quality and completeness."""
    prompt = f"""You are a research report reviewer. Evaluate this report:

TOPIC: {state['topic']}

REPORT:
{state['report']}

Check for:
1. Does it address the topic adequately?
2. Is it well-organized and clear?
3. Are claims supported by the findings?

If the report is good, respond with: APPROVED

If it needs improvement, respond with: REVISE: [specific feedback]

Be reasonable - don't demand perfection."""

    response = llm.invoke(prompt)
    content = response.content.strip()
    
    approved = content.upper().startswith("APPROVED")
    revision_count = state.get("revision_count", 0)
    
    if approved:
        print("✅ Report approved!")
    else:
        print(f"📝 Revision requested (attempt {revision_count + 1})")
    
    return {
        "approved": approved,
        "review_feedback": content if not approved else "",
        "revision_count": revision_count + 1
    }


def should_revise(state: ResearchStateWithReview) -> Literal["revise", "done"]:
    """Decide whether to revise or finish."""
    if state.get("approved", False):
        return "done"
    
    max_rev = state.get("max_revisions", 2)
    if state.get("revision_count", 0) >= max_rev:
        print("⚠️ Max revisions reached, accepting current version")
        return "done"
    
    return "revise"


# Build the enhanced workflow
workflow = StateGraph(ResearchStateWithReview)

workflow.add_node("planner", planner_agent)
workflow.add_node("researcher", researcher_agent)
workflow.add_node("analyst", analyst_agent)
workflow.add_node("writer", writer_with_revision)
workflow.add_node("reviewer", reviewer_agent)

# Main flow
workflow.add_edge(START, "planner")
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "writer")
workflow.add_edge("writer", "reviewer")

# Review loop
workflow.add_conditional_edges(
    "reviewer",
    should_revise,
    {
        "revise": "writer",
        "done": END
    }
)

research_team_v2 = workflow.compile()


if __name__ == "__main__":
    result = research_team_v2.invoke({
        "topic": "Benefits of meditation for stress reduction",
        "questions": [],
        "findings": [],
        "insights": "",
        "report": "",
        "review_feedback": "",
        "revision_count": 0,
        "max_revisions": 2,
        "approved": False
    })
    
    print("\n" + "=" * 60)
    print("FINAL REPORT")
    print("=" * 60)
    print(result["report"])
