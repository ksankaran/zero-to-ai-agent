# From: Zero to AI Agent, Chapter 17, Section 17.5
# Save as: graph_factory.py

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

class ProcessingState(TypedDict):
    text: str
    cleaned: str
    summarized: str
    translated: str
    final_output: str

def clean_text(state: ProcessingState) -> dict:
    """Remove extra whitespace and normalize text."""
    cleaned = " ".join(state["text"].split())
    return {"cleaned": cleaned}

def summarize_text(state: ProcessingState) -> dict:
    """Summarize the text."""
    text = state.get("cleaned") or state["text"]
    response = llm.invoke(f"Summarize in 2 sentences:\n{text}")
    return {"summarized": response.content}

def translate_text(state: ProcessingState) -> dict:
    """Translate to Spanish."""
    text = state.get("summarized") or state.get("cleaned") or state["text"]
    response = llm.invoke(f"Translate to Spanish:\n{text}")
    return {"translated": response.content}

def format_output(state: ProcessingState) -> dict:
    """Compile final output."""
    parts = []
    if state.get("cleaned"):
        parts.append(f"Cleaned: {state['cleaned'][:100]}...")
    if state.get("summarized"):
        parts.append(f"Summary: {state['summarized']}")
    if state.get("translated"):
        parts.append(f"Spanish: {state['translated']}")
    return {"final_output": "\n\n".join(parts)}

# Map of available nodes
AVAILABLE_NODES = {
    "clean": clean_text,
    "summarize": summarize_text,
    "translate": translate_text,
    "format": format_output
}

def build_pipeline_from_config(config: dict):
    """
    Build a graph dynamically from configuration.
    
    Config format:
    {
        "steps": ["clean", "summarize", "translate"],
        "include_format": True
    }
    """
    steps = config.get("steps", [])
    include_format = config.get("include_format", True)
    
    if not steps:
        raise ValueError("Config must include at least one step")
    
    # Validate all steps exist
    for step in steps:
        if step not in AVAILABLE_NODES:
            raise ValueError(f"Unknown step: {step}")
    
    # Build the graph
    graph = StateGraph(ProcessingState)
    
    # Add requested nodes
    for step in steps:
        graph.add_node(step, AVAILABLE_NODES[step])
    
    if include_format:
        graph.add_node("format", AVAILABLE_NODES["format"])
    
    # Connect nodes in sequence
    graph.add_edge(START, steps[0])
    
    for i in range(len(steps) - 1):
        graph.add_edge(steps[i], steps[i + 1])
    
    # Connect last step to format or END
    if include_format:
        graph.add_edge(steps[-1], "format")
        graph.add_edge("format", END)
    else:
        graph.add_edge(steps[-1], END)
    
    return graph.compile()

def test_graph_factory():
    sample_text = """
    Artificial   intelligence   is transforming    how we work.
    Machine learning models can now understand and generate human language
    with remarkable accuracy. This has implications for many industries.
    """
    
    initial_state = {
        "text": sample_text,
        "cleaned": "",
        "summarized": "",
        "translated": "",
        "final_output": ""
    }
    
    # Config 1: Full pipeline
    print("📊 Config 1: Full Pipeline")
    print("=" * 50)
    full_pipeline = build_pipeline_from_config({
        "steps": ["clean", "summarize", "translate"],
        "include_format": True
    })
    result = full_pipeline.invoke(initial_state)
    print(result["final_output"])
    
    # Config 2: Just clean and summarize
    print("\n" + "=" * 50)
    print("📊 Config 2: Clean + Summarize Only")
    print("=" * 50)
    summary_only = build_pipeline_from_config({
        "steps": ["clean", "summarize"],
        "include_format": True
    })
    result = summary_only.invoke(initial_state)
    print(result["final_output"])
    
    # Config 3: Minimal - just clean
    print("\n" + "=" * 50)
    print("📊 Config 3: Clean Only")
    print("=" * 50)
    clean_only = build_pipeline_from_config({
        "steps": ["clean"],
        "include_format": False
    })
    result = clean_only.invoke(initial_state)
    print(f"Cleaned: {result['cleaned']}")

if __name__ == "__main__":
    test_graph_factory()
