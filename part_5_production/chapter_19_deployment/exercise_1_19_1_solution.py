# From: Zero to AI Agent, Chapter 19, Section 19.1
# File: exercise_1_19_1_solution.py (research_agent.py)

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
import operator

# Load environment variables
load_dotenv()

class ResearchState(TypedDict):
    topic: str
    findings: Annotated[list[str], operator.add]
    summary: str

def research_topic(state: ResearchState) -> ResearchState:
    """Research the given topic."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = f"Provide 3 key facts about: {state['topic']}"
    response = llm.invoke(prompt)
    facts = response.content.split("\n")
    return {"findings": facts}

def summarize_findings(state: ResearchState) -> ResearchState:
    """Create a summary from findings."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    findings_text = "\n".join(state["findings"])
    prompt = f"Summarize these findings in one sentence:\n{findings_text}"
    response = llm.invoke(prompt)
    return {"summary": response.content}

# Build the graph
graph = StateGraph(ResearchState)
graph.add_node("research", research_topic)
graph.add_node("summarize", summarize_findings)
graph.add_edge(START, "research")
graph.add_edge("research", "summarize")
graph.add_edge("summarize", END)

agent = graph.compile()

if __name__ == "__main__":
    result = agent.invoke({
        "topic": "renewable energy",
        "findings": [],
        "summary": ""
    })
    print(f"Summary: {result['summary']}")
