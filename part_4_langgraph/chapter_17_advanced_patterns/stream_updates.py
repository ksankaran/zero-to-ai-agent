# From: Zero to AI Agent, Chapter 17, Section 17.2
# Save as: stream_updates.py

import asyncio
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class ResearchState(TypedDict):
    topic: str
    research: str
    analysis: str
    summary: str
    current_step: str

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

async def research_topic(state: ResearchState) -> dict:
    """Gather information about the topic."""
    print("📚 Researching...")
    
    response = await llm.ainvoke(
        f"Provide 3 key facts about: {state['topic']}"
    )
    
    return {
        "research": response.content,
        "current_step": "research_complete"
    }

async def analyze_research(state: ResearchState) -> dict:
    """Analyze the gathered research."""
    print("🔍 Analyzing...")
    
    response = await llm.ainvoke(
        f"Analyze these facts and identify the main theme:\n{state['research']}"
    )
    
    return {
        "analysis": response.content,
        "current_step": "analysis_complete"
    }

async def write_summary(state: ResearchState) -> dict:
    """Write a final summary."""
    print("✍️ Summarizing...")
    
    response = await llm.ainvoke(
        f"Write a one-paragraph summary based on:\n{state['analysis']}"
    )
    
    return {
        "summary": response.content,
        "current_step": "complete"
    }

def build_research_graph():
    workflow = StateGraph(ResearchState)
    
    workflow.add_node("research", research_topic)
    workflow.add_node("analyze", analyze_research)
    workflow.add_node("summarize", write_summary)
    
    workflow.add_edge(START, "research")
    workflow.add_edge("research", "analyze")
    workflow.add_edge("analyze", "summarize")
    workflow.add_edge("summarize", END)
    
    return workflow.compile()

async def run_with_streaming():
    """Run the workflow and stream state updates."""
    
    graph = build_research_graph()
    
    initial_state = {
        "topic": "The history of coffee",
        "research": "",
        "analysis": "",
        "summary": "",
        "current_step": "starting"
    }
    
    print("🚀 Starting research workflow...")
    print("=" * 50)
    
    # stream_mode="updates" gives us just the changes from each node
    async for event in graph.astream(initial_state, stream_mode="updates"):
        # event is a dict: {node_name: {state_updates}}
        for node_name, updates in event.items():
            print(f"\n✅ Node '{node_name}' completed")
            print(f"   Step: {updates.get('current_step', 'N/A')}")
            
            # Show preview of any text content
            for key, value in updates.items():
                if key != "current_step" and isinstance(value, str) and value:
                    preview = value[:100] + "..." if len(value) > 100 else value
                    print(f"   {key}: {preview}")
    
    print("\n" + "=" * 50)
    print("🎉 Workflow complete!")

# Run it
if __name__ == "__main__":
    asyncio.run(run_with_streaming())
