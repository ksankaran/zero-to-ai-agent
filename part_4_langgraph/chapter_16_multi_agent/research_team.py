# From: Zero to AI Agent, Chapter 16, Section 16.5
# File: research_team.py

"""
A multi-agent research assistant team.
Basic sequential version: Planner -> Researcher -> Analyst -> Writer
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# We use a lower temperature for more focused, factual responses
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)


class ResearchState(TypedDict):
    topic: str                    # The research topic
    questions: list[str]          # Research questions from planner
    findings: list[str]           # Raw findings from researcher
    insights: str                 # Analysis from analyst
    report: str                   # Final report from writer
    status: str                   # Current status for tracking


def planner_agent(state: ResearchState) -> dict:
    """
    Takes a topic and creates focused research questions.
    Good research starts with good questions.
    """
    prompt = f"""You are a research planner. Given a topic, create exactly 3 
focused research questions that would help someone understand it thoroughly.

TOPIC: {state['topic']}

Requirements:
- Each question should cover a different aspect
- Questions should be specific and answerable
- Together they should provide comprehensive coverage

Format your response as:
1. [First question]
2. [Second question]
3. [Third question]"""

    response = llm.invoke(prompt)
    
    # Parse the questions from the response
    lines = response.content.strip().split('\n')
    questions = []
    for line in lines:
        # Remove numbering and clean up
        cleaned = line.strip()
        if cleaned and cleaned[0].isdigit():
            # Remove "1. " or "1) " prefix
            cleaned = cleaned[2:].strip() if len(cleaned) > 2 else cleaned
            if cleaned.startswith('.') or cleaned.startswith(')'):
                cleaned = cleaned[1:].strip()
            questions.append(cleaned)
    
    # Ensure we have exactly 3 questions
    questions = questions[:3] if len(questions) >= 3 else questions
    
    print(f"📋 Planner created {len(questions)} research questions")
    for i, q in enumerate(questions, 1):
        print(f"   {i}. {q[:60]}...")
    
    return {
        "questions": questions,
        "status": "questions_ready"
    }


def researcher_agent(state: ResearchState) -> dict:
    """
    Researches each question and gathers findings.
    In production, this might call search APIs or databases.
    """
    findings = []
    
    for i, question in enumerate(state['questions'], 1):
        prompt = f"""You are a research assistant. Answer this research question 
with factual, specific information.

QUESTION: {question}

Provide 2-3 key facts or findings. Be specific and informative.
Keep your response to 3-4 sentences."""

        response = llm.invoke(prompt)
        finding = f"Q{i}: {question}\nFindings: {response.content}"
        findings.append(finding)
        
        print(f"🔍 Researched question {i}/{len(state['questions'])}")
    
    return {
        "findings": findings,
        "status": "research_complete"
    }


def analyst_agent(state: ResearchState) -> dict:
    """
    Analyzes findings to extract key insights and patterns.
    Moves from raw facts to deeper understanding.
    """
    # Combine all findings into one text block
    all_findings = "\n\n".join(state['findings'])
    
    prompt = f"""You are a research analyst. Review these research findings and 
extract key insights.

TOPIC: {state['topic']}

FINDINGS:
{all_findings}

Provide your analysis:
1. What are the 2-3 most important takeaways?
2. Are there any patterns or connections between findings?
3. What's the overall picture that emerges?

Be concise but insightful."""

    response = llm.invoke(prompt)
    
    print("🔬 Analysis complete")
    
    return {
        "insights": response.content,
        "status": "analysis_complete"
    }


def writer_agent(state: ResearchState) -> dict:
    """
    Compiles all research into a readable final report.
    The output the user actually sees.
    """
    all_findings = "\n\n".join(state['findings'])
    
    prompt = f"""You are a research report writer. Create a clear, well-organized 
report based on this research.

TOPIC: {state['topic']}

RESEARCH FINDINGS:
{all_findings}

KEY INSIGHTS:
{state['insights']}

Write a report with:
1. A brief introduction (2-3 sentences)
2. Main findings organized by theme (use bullet points)
3. A conclusion with key takeaways (2-3 sentences)

Keep it concise but comprehensive. Use clear, professional language."""

    response = llm.invoke(prompt)
    
    print("✍️ Report written")
    
    return {
        "report": response.content,
        "status": "complete"
    }


# Build the research workflow
workflow = StateGraph(ResearchState)

# Add all our agents as nodes
workflow.add_node("planner", planner_agent)
workflow.add_node("researcher", researcher_agent)
workflow.add_node("analyst", analyst_agent)
workflow.add_node("writer", writer_agent)

# Connect them in sequence
workflow.add_edge(START, "planner")
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "writer")
workflow.add_edge("writer", END)

# Compile the graph
research_team = workflow.compile()


def run_research(topic: str) -> str:
    """Run the research team on a topic and return the report."""
    
    print("=" * 60)
    print(f"RESEARCHING: {topic}")
    print("=" * 60 + "\n")
    
    result = research_team.invoke({
        "topic": topic,
        "questions": [],
        "findings": [],
        "insights": "",
        "report": "",
        "status": "started"
    })
    
    return result["report"]


# Test it out!
if __name__ == "__main__":
    topic = "The impact of artificial intelligence on healthcare"
    
    report = run_research(topic)
    
    print("\n" + "=" * 60)
    print("FINAL RESEARCH REPORT")
    print("=" * 60)
    print(report)
