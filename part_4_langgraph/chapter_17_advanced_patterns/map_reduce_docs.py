# From: Zero to AI Agent, Chapter 17, Section 17.3
# Save as: map_reduce_docs.py

import operator
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

class MapReduceState(TypedDict):
    documents: list[str]
    summaries: Annotated[list[str], operator.add]
    final_summary: str

class DocumentState(TypedDict):
    document: str
    doc_index: int

def distribute_documents(state: MapReduceState) -> list[Send]:
    """Send each document to a parallel summarization node."""
    return [
        Send("summarize_doc", {"document": doc, "doc_index": i})
        for i, doc in enumerate(state["documents"])
    ]

def summarize_document(state: DocumentState) -> dict:
    """Summarize a single document."""
    response = llm.invoke(
        f"Summarize this text in 2-3 sentences:\n\n{state['document']}"
    )
    
    summary = f"[Doc {state['doc_index'] + 1}] {response.content}"
    print(f"📄 Summarized document {state['doc_index'] + 1}")
    
    return {"summaries": [summary]}

def combine_summaries(state: MapReduceState) -> dict:
    """Reduce: combine all summaries into a final summary."""
    all_summaries = "\n\n".join(state["summaries"])
    
    response = llm.invoke(
        f"Combine these document summaries into one coherent summary:\n\n{all_summaries}"
    )
    
    return {"final_summary": response.content}

def build_map_reduce_graph():
    workflow = StateGraph(MapReduceState)
    
    # We'll use a dummy "start" node to trigger the map
    workflow.add_node("start_map", lambda state: {})
    workflow.add_node("summarize_doc", summarize_document)
    workflow.add_node("reduce", combine_summaries)
    
    workflow.add_edge(START, "start_map")
    
    # Map: distribute to parallel workers
    workflow.add_conditional_edges(
        "start_map",
        distribute_documents,
        ["summarize_doc"]
    )
    
    # Reduce: combine results
    workflow.add_edge("summarize_doc", "reduce")
    workflow.add_edge("reduce", END)
    
    return workflow.compile()

def run_map_reduce():
    graph = build_map_reduce_graph()
    
    # Sample documents (in real use, these could be much longer)
    documents = [
        "Python is a high-level programming language known for its simplicity. "
        "It was created by Guido van Rossum and first released in 1991. "
        "Python emphasizes code readability and allows programmers to express concepts in fewer lines.",
        
        "Machine learning is a subset of artificial intelligence. "
        "It enables computers to learn from data without being explicitly programmed. "
        "Common applications include image recognition and natural language processing.",
        
        "Climate change refers to long-term shifts in global temperatures. "
        "Human activities, particularly burning fossil fuels, are the primary cause. "
        "Effects include rising sea levels, extreme weather, and ecosystem disruption.",
        
        "The Internet of Things connects everyday devices to the internet. "
        "Smart homes, wearables, and industrial sensors are common examples. "
        "IoT is expected to have 75 billion connected devices by 2025."
    ]
    
    print(f"📚 Processing {len(documents)} documents in parallel...")
    print("=" * 50)
    
    result = graph.invoke({
        "documents": documents,
        "summaries": [],
        "final_summary": ""
    })
    
    print("\n" + "=" * 50)
    print(f"✅ Processed {len(result['summaries'])} documents")
    print(f"\n📝 Final Combined Summary:\n{result['final_summary']}")

if __name__ == "__main__":
    run_map_reduce()
