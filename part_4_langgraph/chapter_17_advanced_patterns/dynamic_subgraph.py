# From: Zero to AI Agent, Chapter 17, Section 17.5
# Save as: dynamic_subgraph.py

from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

class MainState(TypedDict):
    documents: list[str]
    processing_type: str  # "quick", "thorough", "deep"
    results: Annotated[list[str], operator.add]
    summary: str

def build_processing_subgraph(processing_type: str):
    """Build different subgraphs based on processing type."""
    
    class SubState(TypedDict):
        doc: str
        processed: str
    
    def basic_process(state: SubState) -> dict:
        return {"processed": f"[Basic] {state['doc'][:50]}..."}
    
    def detailed_process(state: SubState) -> dict:
        response = llm.invoke(f"Summarize: {state['doc']}")
        return {"processed": f"[Detailed] {response.content}"}
    
    def deep_analysis(state: SubState) -> dict:
        response = llm.invoke(
            f"Provide deep analysis with insights: {state['doc']}"
        )
        return {"processed": f"[Deep] {response.content}"}
    
    def quality_check(state: SubState) -> dict:
        return {"processed": state["processed"] + " ✓ Verified"}
    
    subgraph = StateGraph(SubState)
    
    if processing_type == "quick":
        # Quick: just basic processing
        subgraph.add_node("process", basic_process)
        subgraph.add_edge(START, "process")
        subgraph.add_edge("process", END)
    
    elif processing_type == "thorough":
        # Thorough: detailed + quality check
        subgraph.add_node("process", detailed_process)
        subgraph.add_node("verify", quality_check)
        subgraph.add_edge(START, "process")
        subgraph.add_edge("process", "verify")
        subgraph.add_edge("verify", END)
    
    else:  # deep
        # Deep: analysis + quality check
        subgraph.add_node("analyze", deep_analysis)
        subgraph.add_node("verify", quality_check)
        subgraph.add_edge(START, "analyze")
        subgraph.add_edge("analyze", "verify")
        subgraph.add_edge("verify", END)
    
    return subgraph.compile()

def process_documents(state: MainState) -> dict:
    """Process each document using dynamically created subgraph."""
    
    # Build subgraph based on processing type
    subgraph = build_processing_subgraph(state["processing_type"])
    
    results = []
    for i, doc in enumerate(state["documents"]):
        print(f"  Processing document {i + 1}...")
        
        # Run subgraph for each document
        sub_result = subgraph.invoke({
            "doc": doc,
            "processed": ""
        })
        
        results.append(sub_result["processed"])
    
    return {"results": results}

def summarize_all(state: MainState) -> dict:
    """Summarize all results."""
    summary = f"Processed {len(state['results'])} documents:\n"
    for i, r in enumerate(state["results"], 1):
        summary += f"\n{i}. {r[:100]}..."
    return {"summary": summary}

def build_main_graph():
    """Build the main orchestrating graph."""
    
    graph = StateGraph(MainState)
    
    graph.add_node("process", process_documents)
    graph.add_node("summarize", summarize_all)
    
    graph.add_edge(START, "process")
    graph.add_edge("process", "summarize")
    graph.add_edge("summarize", END)
    
    return graph.compile()

def test_dynamic_subgraph():
    docs = [
        "AI is transforming healthcare with better diagnostics.",
        "Renewable energy adoption is accelerating globally.",
        "Remote work has changed corporate culture permanently."
    ]
    
    main_graph = build_main_graph()
    
    for proc_type in ["quick", "thorough", "deep"]:
        print("\n" + "=" * 60)
        print(f"📊 Processing Type: {proc_type.upper()}")
        print("=" * 60)
        
        result = main_graph.invoke({
            "documents": docs,
            "processing_type": proc_type,
            "results": [],
            "summary": ""
        })
        
        print(result["summary"])

if __name__ == "__main__":
    test_dynamic_subgraph()
