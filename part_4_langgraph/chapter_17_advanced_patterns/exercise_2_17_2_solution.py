# From: Zero to AI Agent, Chapter 17, Section 17.2
# Save as: exercise_2_17_2_solution.py
# Exercise 2: File Processor Simulation

import asyncio
import random
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import StreamWriter
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class FileProcessState(TypedDict):
    filenames: list[str]
    processed: list[dict]
    errors: list[dict]
    summary: str
    status: str

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, streaming=True)

def create_progress_bar(progress: float, width: int = 20) -> str:
    """Create ASCII progress bar."""
    filled = int(width * progress / 100)
    empty = width - filled
    return f"[{'█' * filled}{'░' * empty}] {progress:.0f}%"

async def process_files(state: FileProcessState, writer: StreamWriter) -> dict:
    """Process each file with progress bar updates."""
    
    files = state["filenames"]
    processed = []
    errors = []
    
    total = len(files)
    
    writer({
        "type": "start",
        "message": f"Starting to process {total} files...\n"
    })
    
    for i, filename in enumerate(files):
        progress = (i / total) * 100
        
        # Stage 1: Validating
        writer({
            "type": "progress",
            "progress_bar": create_progress_bar(progress),
            "stage": "Validating",
            "file": filename
        })
        await asyncio.sleep(0.2)
        
        # Simulate random validation error (10% chance)
        if random.random() < 0.1:
            errors.append({
                "file": filename,
                "error": "Validation failed: Invalid file format",
                "stage": "validation"
            })
            writer({
                "type": "error",
                "message": f"  ❌ {filename}: Validation failed"
            })
            continue
        
        # Stage 2: Processing
        writer({
            "type": "progress",
            "progress_bar": create_progress_bar(progress + (100/total/3)),
            "stage": "Processing",
            "file": filename
        })
        await asyncio.sleep(0.3)
        
        # Simulate random processing error (5% chance)
        if random.random() < 0.05:
            errors.append({
                "file": filename,
                "error": "Processing failed: Corrupted data",
                "stage": "processing"
            })
            writer({
                "type": "error",
                "message": f"  ❌ {filename}: Processing failed"
            })
            continue
        
        # Stage 3: Saving
        writer({
            "type": "progress",
            "progress_bar": create_progress_bar(progress + (100/total*2/3)),
            "stage": "Saving",
            "file": filename
        })
        await asyncio.sleep(0.2)
        
        # Success!
        processed.append({
            "file": filename,
            "result": f"Processed successfully",
            "size": random.randint(100, 10000)
        })
        
        writer({
            "type": "success",
            "message": f"  ✅ {filename}: Completed"
        })
    
    # Final progress
    writer({
        "type": "progress",
        "progress_bar": create_progress_bar(100),
        "stage": "Complete",
        "file": "All files"
    })
    
    return {
        "processed": processed,
        "errors": errors,
        "status": "files_processed"
    }

async def generate_summary(state: FileProcessState, writer: StreamWriter) -> dict:
    """Generate a summary report using LLM."""
    
    writer({
        "type": "status",
        "message": "\n📊 Generating summary report..."
    })
    
    success_count = len(state["processed"])
    error_count = len(state["errors"])
    total = success_count + error_count
    
    error_details = "\n".join([
        f"- {e['file']}: {e['error']}" 
        for e in state["errors"]
    ]) if state["errors"] else "No errors"
    
    prompt = f"""Generate a brief file processing summary report:
    
    Total files: {total}
    Successfully processed: {success_count}
    Failed: {error_count}
    Success rate: {(success_count/total*100) if total > 0 else 0:.1f}%
    
    Errors encountered:
    {error_details}
    
    Write a professional 2-3 sentence summary."""
    
    response = await llm.ainvoke(prompt)
    
    return {"summary": response.content, "status": "complete"}

def build_file_processor_graph():
    workflow = StateGraph(FileProcessState)
    
    workflow.add_node("process", process_files)
    workflow.add_node("summarize", generate_summary)
    
    workflow.add_edge(START, "process")
    workflow.add_edge("process", "summarize")
    workflow.add_edge("summarize", END)
    
    return workflow.compile()

async def run_file_processor():
    """Run the file processor with streaming progress."""
    
    graph = build_file_processor_graph()
    
    # Sample filenames
    filenames = [
        "report_2024.pdf",
        "data_export.csv",
        "config.json",
        "image_001.png",
        "backup.zip",
        "notes.txt",
        "analysis.xlsx",
        "presentation.pptx"
    ]
    
    initial_state = {
        "filenames": filenames,
        "processed": [],
        "errors": [],
        "summary": "",
        "status": "starting"
    }
    
    print("📁 File Processor Simulation")
    print("=" * 60)
    print(f"Processing {len(filenames)} files...\n")
    
    final_summary = ""
    success_count = 0
    error_count = 0
    
    async for mode, chunk in graph.astream(
        initial_state,
        stream_mode=["updates", "custom"]
    ):
        if mode == "custom":
            msg_type = chunk.get("type", "")
            
            if msg_type == "progress":
                bar = chunk.get("progress_bar", "")
                stage = chunk.get("stage", "")
                file = chunk.get("file", "")
                # Print progress bar on same line
                print(f"\r{bar} {stage}: {file:<30}", end="", flush=True)
            elif msg_type in ["success", "error", "status", "start"]:
                print()  # New line before message
                print(chunk.get("message", ""))
                
        elif mode == "updates":
            for node_name, updates in chunk.items():
                if "processed" in updates:
                    success_count = len(updates["processed"])
                if "errors" in updates:
                    error_count = len(updates["errors"])
                if "summary" in updates:
                    final_summary = updates["summary"]
    
    print("\n" + "=" * 60)
    print("📊 FINAL REPORT")
    print("-" * 60)
    print(f"✅ Successfully processed: {success_count}")
    print(f"❌ Failed: {error_count}")
    print(f"📈 Success rate: {(success_count/(success_count+error_count)*100):.1f}%")
    print("-" * 60)
    print(f"Summary: {final_summary}")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_file_processor())
