# From: Zero to AI Agent, Chapter 16, Section 16.1
# File: multi_agent_demo.py

"""
Demonstrates specialized agents as graph nodes.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


class ReportState(TypedDict):
    raw_text: str
    analysis: str
    summary: str


def analyst_agent(state: ReportState) -> dict:
    """Data Analyst Agent - extracts metrics and signals."""
    prompt = """You are a data analyst. Your ONLY job is to:
    - Extract key metrics and statistics
    - Identify positive and negative signals
    - Note any risks or concerns
    Be precise. Use numbers. Format as bullet points."""
    
    response = llm.invoke(f"{prompt}\n\nAnalyze:\n{state['raw_text']}")
    return {"analysis": response.content}


def summarizer_agent(state: ReportState) -> dict:
    """Executive Summarizer Agent - creates brief summaries."""
    prompt = """You are an executive communication specialist.
    Write a 2-3 sentence summary for busy executives.
    Lead with the most important finding."""
    
    response = llm.invoke(f"{prompt}\n\nBased on:\n{state['analysis']}")
    return {"summary": response.content}


# Build the multi-agent graph
workflow = StateGraph(ReportState)

# Add our specialist agents as nodes
workflow.add_node("analyst", analyst_agent)
workflow.add_node("summarizer", summarizer_agent)

# Define the flow: analyst first, then summarizer
workflow.add_edge(START, "analyst")
workflow.add_edge("analyst", "summarizer")
workflow.add_edge("summarizer", END)

# Compile the graph
app = workflow.compile()

# Run the multi-agent system
result = app.invoke({
    "raw_text": """The new product launch exceeded expectations. Sales were up 
    150% compared to our previous launch. Customer feedback has been 
    overwhelmingly positive, with 92% satisfaction ratings. However, 
    we did face some supply chain challenges that delayed shipments 
    to certain regions by 2-3 weeks.""",
    "analysis": "",
    "summary": ""
})

print("=== Analyst Agent Output ===")
print(result["analysis"])
print("\n=== Summarizer Agent Output ===")
print(result["summary"])
