# From: Building AI Agents, Chapter 14, Section 14.6
# File: exercise_3_14_6_solution.py

"""Research assistant with retry logic for low-quality results.

Exercise 3 Solution: Enhance a research assistant to handle poor-quality results:
- If search quality is LOW, retry with a modified query
- Track retries per search (max 2 retries)
- If still low after retries, move on to next search

Key insight: retry creates a mini-loop within the larger search loop.
"""

import os
import random
from typing import TypedDict, Annotated
from operator import add
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


# === STATE ===

class ResearchState(TypedDict):
    question: str
    search_queries: Annotated[list, add]
    findings: Annotated[list, add]
    current_query: str            # The active query
    current_quality: str          # HIGH, MEDIUM, LOW
    retry_count: int              # Retries for THIS search
    max_retries: int              # Limit per search (e.g., 2)
    search_count: int             # Total searches done
    max_searches: int             # Overall limit
    has_enough_info: bool         # Do we have enough?
    final_answer: str


# === NODES ===

def generate_search_query(state: ResearchState) -> dict:
    """Generate a search query based on the question and existing findings."""
    question = state["question"]
    findings = state.get("findings", [])
    
    if not findings:
        # First query - base it on the question
        prompt = f"Generate a concise search query for: {question}"
    else:
        # Subsequent queries - look for gaps
        prompt = f"""Question: {question}
        
        Already found: {len(findings)} results.
        
        Generate a NEW search query to find additional information."""
    
    response = llm.invoke(prompt)
    query = response.content.strip()
    
    print(f"🔍 New query: {query}")
    
    return {
        "current_query": query,
        "search_queries": [query],
        "search_count": state.get("search_count", 0) + 1,
        "retry_count": 0  # Reset retry count for new search
    }


def perform_search(state: ResearchState) -> dict:
    """Search and assess result quality."""
    query = state["current_query"]
    
    # Simulate search
    prompt = f"Simulate a search result for: {query}\nProvide a brief finding."
    response = llm.invoke(prompt)
    finding = response.content.strip()
    
    # Simulate quality (higher retry = better chance)
    # In real app, would actually assess the result
    quality_score = random.random() + (state["retry_count"] * 0.3)
    if quality_score > 0.7:
        quality = "HIGH"
    elif quality_score > 0.4:
        quality = "MEDIUM"
    else:
        quality = "LOW"
    
    print(f"📄 Quality: {quality}")
    
    return {
        "findings": [{"query": query, "result": finding, "quality": quality}],
        "current_quality": quality
    }


def route_after_search(state: ResearchState) -> str:
    """Decide: accept, retry, or move on."""
    quality = state["current_quality"]
    retry_count = state["retry_count"]
    max_retries = state["max_retries"]
    
    # High quality: accept
    if quality == "HIGH":
        print("✅ Good quality - accepting")
        return "evaluate"
    
    # Low quality with retries left: retry
    if quality == "LOW" and retry_count < max_retries:
        print(f"🔄 Low quality - retry {retry_count + 1}/{max_retries}")
        return "retry_search"
    
    # Medium or exhausted retries: accept and move on
    print("⚠️ Accepting (medium quality or max retries)")
    return "evaluate"


def retry_search(state: ResearchState) -> dict:
    """Modify query and increment retry count."""
    query = state["current_query"]
    
    prompt = f'The search "{query}" gave poor results. Suggest a better query.'
    response = llm.invoke(prompt)
    new_query = response.content.strip()
    
    print(f"🔄 Retry with: {new_query}")
    
    return {
        "current_query": new_query,
        "retry_count": state["retry_count"] + 1
    }


def evaluate_findings(state: ResearchState) -> dict:
    """Evaluate if we have enough information."""
    findings = state["findings"]
    question = state["question"]
    
    # Simple evaluation: do we have at least 2 high/medium quality findings?
    good_findings = [f for f in findings if f.get("quality") in ["HIGH", "MEDIUM"]]
    has_enough = len(good_findings) >= 2
    
    print(f"📊 Evaluation: {len(good_findings)} good findings, enough={has_enough}")
    
    return {"has_enough_info": has_enough}


def route_after_evaluate(state: ResearchState) -> str:
    """Decide: search more or synthesize answer."""
    has_enough = state["has_enough_info"]
    search_count = state["search_count"]
    max_searches = state["max_searches"]
    
    # Safety valve: stop at max searches
    if search_count >= max_searches:
        print(f"🛑 Max searches ({max_searches}) reached")
        return "synthesize"
    
    # Enough info: done
    if has_enough:
        print("✅ Enough info gathered")
        return "synthesize"
    
    # Otherwise, keep searching
    return "search_more"


def synthesize_answer(state: ResearchState) -> dict:
    """Synthesize final answer from findings."""
    findings = state["findings"]
    question = state["question"]
    
    findings_text = "\n".join([f"- {f['result']}" for f in findings])
    
    prompt = f"""Based on these findings, answer the question.
    
    Question: {question}
    
    Findings:
    {findings_text}
    
    Provide a concise answer."""
    
    response = llm.invoke(prompt)
    
    print("📝 Answer synthesized")
    
    return {"final_answer": response.content}


# === GRAPH BUILDER ===

def create_research_graph():
    """Build the research assistant graph with retry logic.
    
    Two levels of looping:
    1. Outer loop: search → evaluate → maybe search again
    2. Inner loop: search → quality check → maybe retry same search
    """
    graph = StateGraph(ResearchState)
    
    graph.add_node("generate_query", generate_search_query)
    graph.add_node("search", perform_search)
    graph.add_node("retry_search", retry_search)
    graph.add_node("evaluate", evaluate_findings)
    graph.add_node("synthesize", synthesize_answer)
    
    graph.set_entry_point("generate_query")
    
    graph.add_edge("generate_query", "search")
    
    # After search: accept, retry, or evaluate
    graph.add_conditional_edges("search", route_after_search, {
        "retry_search": "retry_search",
        "evaluate": "evaluate"
    })
    
    # Retry loops back to search
    graph.add_edge("retry_search", "search")
    
    # After evaluate: more searching or synthesize
    graph.add_conditional_edges("evaluate", route_after_evaluate, {
        "search_more": "generate_query",
        "synthesize": "synthesize"
    })
    
    graph.add_edge("synthesize", END)
    
    return graph.compile()


# === MAIN ===

def main():
    app = create_research_graph()
    
    print("=" * 60)
    print("🔬 Research Assistant with Retry Logic")
    print("=" * 60)
    
    result = app.invoke({
        "question": "What are the main benefits of using TypeScript over JavaScript?",
        "search_queries": [],
        "findings": [],
        "current_query": "",
        "current_quality": "",
        "retry_count": 0,
        "max_retries": 2,
        "search_count": 0,
        "max_searches": 4,
        "has_enough_info": False,
        "final_answer": ""
    })
    
    print("\n" + "=" * 60)
    print("📋 Final Answer:")
    print("=" * 60)
    print(result["final_answer"])
    print(f"\n📊 Stats: {result['search_count']} searches, {len(result['findings'])} findings")


if __name__ == "__main__":
    main()
