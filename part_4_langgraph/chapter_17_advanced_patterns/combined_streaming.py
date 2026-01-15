# From: Zero to AI Agent, Chapter 17, Section 17.2
# Save as: combined_streaming.py

import asyncio
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import StreamWriter
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class AnalysisState(TypedDict):
    query: str
    result: str
    status: str

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

async def analyze_query(state: AnalysisState, writer: StreamWriter) -> dict:
    """Analyze a query with progress updates."""
    
    writer({"phase": "starting", "message": "Beginning analysis..."})
    
    await asyncio.sleep(0.3)
    
    writer({"phase": "thinking", "message": "Formulating response..."})
    
    response = await llm.ainvoke(f"Briefly analyze: {state['query']}")
    
    writer({"phase": "complete", "message": "Analysis complete!"})
    
    return {
        "result": response.content,
        "status": "done"
    }

def build_analysis_graph():
    workflow = StateGraph(AnalysisState)
    workflow.add_node("analyze", analyze_query)
    workflow.add_edge(START, "analyze")
    workflow.add_edge("analyze", END)
    return workflow.compile()

async def run_combined_streaming():
    """Demonstrate combined streaming modes."""
    
    graph = build_analysis_graph()
    
    initial_state = {
        "query": "What makes Python popular for AI development?",
        "result": "",
        "status": "pending"
    }
    
    print("🔍 Running analysis with combined streaming...")
    print("=" * 50)
    
    # Combine "updates" and "custom" modes
    async for mode, chunk in graph.astream(
        initial_state, 
        stream_mode=["updates", "custom"]
    ):
        if mode == "custom":
            # Our custom progress updates
            print(f"  📡 {chunk.get('message', chunk)}")
        elif mode == "updates":
            # State updates from nodes
            for node_name, updates in chunk.items():
                print(f"  ✅ Node '{node_name}' updated state")
                if updates.get("result"):
                    preview = updates["result"][:80] + "..."
                    print(f"     Result: {preview}")
    
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(run_combined_streaming())
