# From: Zero to AI Agent, Chapter 17, Section 17.2
# Save as: custom_streaming.py

import asyncio
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import StreamWriter
from dotenv import load_dotenv

load_dotenv()

class ProcessingState(TypedDict):
    items: list[str]
    results: list[str]
    status: str

async def process_items(state: ProcessingState, writer: StreamWriter) -> dict:
    """Process items with progress updates."""
    
    items = state["items"]
    results = []
    
    # Send initial status
    writer({"status": "starting", "message": f"Processing {len(items)} items..."})
    
    for i, item in enumerate(items):
        # Send progress update for each item
        progress = (i + 1) / len(items) * 100
        writer({
            "status": "processing",
            "current_item": item,
            "progress": f"{progress:.0f}%",
            "message": f"Processing item {i + 1}/{len(items)}: {item}"
        })
        
        # Simulate processing time
        await asyncio.sleep(0.5)
        
        # Process the item (just uppercase for demo)
        results.append(item.upper())
    
    # Send completion status
    writer({"status": "complete", "message": "All items processed!"})
    
    return {"results": results, "status": "complete"}

def build_processing_graph():
    workflow = StateGraph(ProcessingState)
    workflow.add_node("process", process_items)
    workflow.add_edge(START, "process")
    workflow.add_edge("process", END)
    return workflow.compile()

async def run_with_progress():
    """Run workflow with custom progress streaming."""
    
    graph = build_processing_graph()
    
    initial_state = {
        "items": ["apple", "banana", "cherry", "date", "elderberry"],
        "results": [],
        "status": "pending"
    }
    
    print("🔄 Processing with live progress...")
    print("=" * 50)
    
    # Use stream_mode="custom" to receive our custom data
    async for chunk in graph.astream(initial_state, stream_mode="custom"):
        # chunk contains our custom data from writer()
        status = chunk.get("status", "")
        message = chunk.get("message", "")
        progress = chunk.get("progress", "")
        
        if progress:
            print(f"  [{progress}] {message}")
        else:
            print(f"  {message}")
    
    print("=" * 50)
    print("✅ Done!")

if __name__ == "__main__":
    asyncio.run(run_with_progress())
