# From: Zero to AI Agent, Chapter 17, Section 17.4
# Save as: component_library.py

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


# =============================================================================
# SHARED STATE
# =============================================================================

class WorkflowState(TypedDict):
    input_text: str
    summary: str
    sentiment: str
    keywords: list[str]
    translation: str
    final_output: str


# =============================================================================
# CORE FUNCTIONS (defined once, reused everywhere)
# =============================================================================

def summarize(state: WorkflowState) -> dict:
    """Summarize input text."""
    response = llm.invoke(
        f"Summarize this in 2 sentences:\n{state['input_text']}"
    )
    return {"summary": response.content}


def analyze_sentiment(state: WorkflowState) -> dict:
    """Analyze sentiment of input text."""
    response = llm.invoke(
        f"What is the sentiment of this text? "
        f"Answer POSITIVE, NEGATIVE, or NEUTRAL:\n{state['input_text']}"
    )
    sentiment = response.content.strip().upper()
    if sentiment not in ["POSITIVE", "NEGATIVE", "NEUTRAL"]:
        sentiment = "NEUTRAL"
    return {"sentiment": sentiment}


def extract_keywords(state: WorkflowState) -> dict:
    """Extract keywords from input text."""
    response = llm.invoke(
        f"Extract 5 keywords from this text as a comma-separated list:\n{state['input_text']}"
    )
    keywords = [k.strip() for k in response.content.split(",")]
    return {"keywords": keywords[:5]}


def compile_results(state: WorkflowState) -> dict:
    """Compile all analysis results into final output."""
    output = (
        f"📝 Summary: {state['summary']}\n"
        f"😊 Sentiment: {state['sentiment']}\n"
        f"🔑 Keywords: {', '.join(state['keywords'])}"
    )
    return {"final_output": output}


# =============================================================================
# SUBGRAPH WRAPPERS (for modular/sequential composition)
# =============================================================================

def build_summarizer():
    """Reusable summarization component."""
    graph = StateGraph(WorkflowState)
    graph.add_node("summarize", summarize)  # Reuse core function
    graph.add_edge(START, "summarize")
    graph.add_edge("summarize", END)
    return graph.compile()


def build_sentiment_analyzer():
    """Reusable sentiment analysis component."""
    graph = StateGraph(WorkflowState)
    graph.add_node("sentiment", analyze_sentiment)  # Reuse core function
    graph.add_edge(START, "sentiment")
    graph.add_edge("sentiment", END)
    return graph.compile()


def build_keyword_extractor():
    """Reusable keyword extraction component."""
    graph = StateGraph(WorkflowState)
    graph.add_node("keywords", extract_keywords)  # Reuse core function
    graph.add_edge(START, "keywords")
    graph.add_edge("keywords", END)
    return graph.compile()


# =============================================================================
# SEQUENTIAL PIPELINE (uses subgraphs)
# =============================================================================

def build_analysis_pipeline():
    """Compose components into a sequential analysis pipeline.
    
    Uses compiled subgraphs - works great for sequential flows.
    """
    summarizer = build_summarizer()
    sentiment_analyzer = build_sentiment_analyzer()
    keyword_extractor = build_keyword_extractor()
    
    pipeline = StateGraph(WorkflowState)
    
    # Add subgraphs as nodes
    pipeline.add_node("summarize", summarizer)
    pipeline.add_node("sentiment", sentiment_analyzer)
    pipeline.add_node("keywords", keyword_extractor)
    pipeline.add_node("compile", compile_results)
    
    # Sequential flow
    pipeline.add_edge(START, "summarize")
    pipeline.add_edge("summarize", "sentiment")
    pipeline.add_edge("sentiment", "keywords")
    pipeline.add_edge("keywords", "compile")
    pipeline.add_edge("compile", END)
    
    return pipeline.compile()


# =============================================================================
# PARALLEL PIPELINE (uses functions directly)
# =============================================================================

def build_parallel_analysis():
    """Run analysis components in parallel.
    
    Uses functions directly instead of subgraphs. Compiled subgraphs
    can't run in parallel because they process the full state, causing
    concurrent update conflicts on shared input fields.
    """
    pipeline = StateGraph(WorkflowState)
    
    # Use core functions directly for parallel execution
    pipeline.add_node("summarize", summarize)
    pipeline.add_node("sentiment", analyze_sentiment)
    pipeline.add_node("keywords", extract_keywords)
    pipeline.add_node("compile", compile_results)
    
    # Parallel: all three start from START
    pipeline.add_edge(START, "summarize")
    pipeline.add_edge(START, "sentiment")
    pipeline.add_edge(START, "keywords")
    
    # All converge to compile
    pipeline.add_edge("summarize", "compile")
    pipeline.add_edge("sentiment", "compile")
    pipeline.add_edge("keywords", "compile")
    
    pipeline.add_edge("compile", END)
    
    return pipeline.compile()


# =============================================================================
# DEMO
# =============================================================================

def run_component_library_example():
    sample_text = """
    Artificial intelligence is transforming healthcare in remarkable ways.
    From early disease detection to personalized treatment plans, AI is
    helping doctors provide better care. However, concerns about privacy
    and the need for human oversight remain important considerations.
    """
    
    initial_state = {
        "input_text": sample_text,
        "summary": "",
        "sentiment": "",
        "keywords": [],
        "translation": "",
        "final_output": ""
    }
    
    # Test sequential pipeline
    print("📊 Sequential Analysis Pipeline")
    print("=" * 50)
    sequential = build_analysis_pipeline()
    result = sequential.invoke(initial_state)
    print(result["final_output"])
    
    print("\n" + "=" * 50)
    
    # Test parallel pipeline
    print("⚡ Parallel Analysis Pipeline")
    print("=" * 50)
    parallel = build_parallel_analysis()
    result = parallel.invoke(initial_state)
    print(result["final_output"])


if __name__ == "__main__":
    run_component_library_example()