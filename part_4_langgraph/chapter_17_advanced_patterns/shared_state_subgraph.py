# From: Zero to AI Agent, Chapter 17, Section 17.4
# Save as: shared_state_subgraph.py

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

class SharedState(TypedDict):
    topic: str
    research: str
    analysis: str
    final_report: str

def build_research_subgraph():
    """Build a reusable research subgraph."""
    
    def gather_info(state: SharedState) -> dict:
        """Gather information about the topic."""
        response = llm.invoke(
            f"Provide 3 key facts about: {state['topic']}"
        )
        return {"research": response.content}
    
    def analyze_info(state: SharedState) -> dict:
        """Analyze the gathered information."""
        response = llm.invoke(
            f"Analyze these facts and identify patterns:\n{state['research']}"
        )
        return {"analysis": response.content}
    
    # Build the subgraph
    subgraph = StateGraph(SharedState)
    subgraph.add_node("gather", gather_info)
    subgraph.add_node("analyze", analyze_info)
    
    subgraph.add_edge(START, "gather")
    subgraph.add_edge("gather", "analyze")
    subgraph.add_edge("analyze", END)
    
    return subgraph.compile()

def build_parent_graph():
    """Build parent graph that uses the research subgraph."""
    
    # Get our compiled subgraph
    research_subgraph = build_research_subgraph()
    
    def write_report(state: SharedState) -> dict:
        """Write final report based on research and analysis."""
        response = llm.invoke(
            f"Write a brief report about {state['topic']}.\n"
            f"Research: {state['research']}\n"
            f"Analysis: {state['analysis']}"
        )
        return {"final_report": response.content}
    
    # Build parent graph
    parent = StateGraph(SharedState)
    
    # Add the subgraph as a node!
    parent.add_node("research", research_subgraph)
    parent.add_node("report", write_report)
    
    parent.add_edge(START, "research")
    parent.add_edge("research", "report")
    parent.add_edge("report", END)
    
    return parent.compile()

def run_shared_state_example():
    graph = build_parent_graph()
    
    result = graph.invoke({
        "topic": "renewable energy",
        "research": "",
        "analysis": "",
        "final_report": ""
    })
    
    print("📊 Subgraph Example: Shared State")
    print("=" * 50)
    print(f"\nTopic: {result['topic']}")
    print(f"\n📚 Research:\n{result['research'][:200]}...")
    print(f"\n🔍 Analysis:\n{result['analysis'][:200]}...")
    print(f"\n📝 Final Report:\n{result['final_report']}")

if __name__ == "__main__":
    run_shared_state_example()
