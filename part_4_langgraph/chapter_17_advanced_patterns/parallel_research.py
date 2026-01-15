# From: Zero to AI Agent, Chapter 17, Section 17.3
# Save as: parallel_research.py

import operator
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class ResearchState(TypedDict):
    topic: str
    # This field will receive results from parallel nodes
    # operator.add means: combine by extending the list
    findings: Annotated[list[str], operator.add]
    summary: str

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

def search_wikipedia(state: ResearchState) -> dict:
    """Simulate searching Wikipedia."""
    response = llm.invoke(
        f"You are Wikipedia. Give 2 key facts about: {state['topic']}"
    )
    return {"findings": [f"[Wikipedia] {response.content}"]}

def search_academic(state: ResearchState) -> dict:
    """Simulate searching academic papers."""
    response = llm.invoke(
        f"You are an academic database. Give 2 scholarly insights about: {state['topic']}"
    )
    return {"findings": [f"[Academic] {response.content}"]}

def search_news(state: ResearchState) -> dict:
    """Simulate searching recent news."""
    response = llm.invoke(
        f"You are a news service. Give 2 recent developments about: {state['topic']}"
    )
    return {"findings": [f"[News] {response.content}"]}

def synthesize_findings(state: ResearchState) -> dict:
    """Combine all findings into a summary."""
    all_findings = "\n\n".join(state["findings"])
    
    response = llm.invoke(
        f"Synthesize these research findings into a brief summary:\n\n{all_findings}"
    )
    return {"summary": response.content}

def build_parallel_research_graph():
    workflow = StateGraph(ResearchState)
    
    # Add all nodes
    workflow.add_node("wikipedia", search_wikipedia)
    workflow.add_node("academic", search_academic)
    workflow.add_node("news", search_news)
    workflow.add_node("synthesize", synthesize_findings)
    
    # Fan-out: START connects to all three search nodes
    workflow.add_edge(START, "wikipedia")
    workflow.add_edge(START, "academic")
    workflow.add_edge(START, "news")
    
    # Fan-in: All search nodes connect to synthesize
    workflow.add_edge("wikipedia", "synthesize")
    workflow.add_edge("academic", "synthesize")
    workflow.add_edge("news", "synthesize")
    
    # End after synthesis
    workflow.add_edge("synthesize", END)
    
    return workflow.compile()

def run_parallel_research():
    graph = build_parallel_research_graph()
    
    result = graph.invoke({
        "topic": "renewable energy",
        "findings": [],
        "summary": ""
    })
    
    print("🔬 Parallel Research Results")
    print("=" * 50)
    print(f"\nTopic: {result['topic']}")
    print(f"\nFindings from {len(result['findings'])} sources:")
    for finding in result["findings"]:
        print(f"\n{finding[:200]}...")
    print(f"\n📝 Summary:\n{result['summary']}")

if __name__ == "__main__":
    run_parallel_research()
