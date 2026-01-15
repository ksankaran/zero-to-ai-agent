# From: Zero to AI Agent, Chapter 15, Section 15.6
# File: exercise_3_15_6_solution.py

"""
Document analyzer with graceful feature degradation.
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END
import random

class AnalysisState(TypedDict):
    document: str
    features: dict
    warnings: Annotated[list[str], add]

def count_words(state: AnalysisState) -> dict:
    """Core feature - always works."""
    word_count = len(state["document"].split())
    features = state.get("features", {})
    features["word_count"] = {"value": word_count, "status": "ok"}
    return {"features": features}

def analyze_sentiment(state: AnalysisState) -> dict:
    """Optional - fails 40% of the time."""
    features = state.get("features", {})
    
    if random.random() < 0.4:
        features["sentiment"] = {"value": None, "status": "failed"}
        return {
            "features": features,
            "warnings": ["Sentiment analysis unavailable"]
        }
    
    features["sentiment"] = {"value": "positive", "status": "ok"}
    return {"features": features}

def extract_keywords(state: AnalysisState) -> dict:
    """Optional - fails 30% of the time."""
    features = state.get("features", {})
    
    if random.random() < 0.3:
        features["keywords"] = {"value": None, "status": "failed"}
        return {
            "features": features,
            "warnings": ["Keyword extraction unavailable"]
        }
    
    words = state["document"].split()[:3]
    features["keywords"] = {"value": words, "status": "ok"}
    return {"features": features}

def summarize(state: AnalysisState) -> dict:
    """Optional - fails 50% of the time."""
    features = state.get("features", {})
    
    if random.random() < 0.5:
        features["summary"] = {"value": None, "status": "failed"}
        return {
            "features": features,
            "warnings": ["Summarization unavailable"]
        }
    
    summary = state["document"][:50] + "..."
    features["summary"] = {"value": summary, "status": "ok"}
    return {"features": features}

# Build graph
graph = StateGraph(AnalysisState)
graph.add_node("words", count_words)
graph.add_node("sentiment", analyze_sentiment)
graph.add_node("keywords", extract_keywords)
graph.add_node("summary", summarize)

graph.add_edge(START, "words")
graph.add_edge("words", "sentiment")
graph.add_edge("sentiment", "keywords")
graph.add_edge("keywords", "summary")
graph.add_edge("summary", END)

app = graph.compile()

# Test
doc = "This is a sample document for testing the analyzer features."
result = app.invoke({"document": doc, "features": {}, "warnings": []})

print("=== Document Analysis Results ===\n")

for feature, data in result["features"].items():
    status = "✓" if data["status"] == "ok" else "✗"
    value = data["value"] if data["value"] else "N/A"
    print(f"{status} {feature}: {value}")

if result["warnings"]:
    print(f"\n⚠️ Warnings: {len(result['warnings'])}")
    for w in result["warnings"]:
        print(f"  - {w}")
