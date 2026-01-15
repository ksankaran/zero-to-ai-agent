# From: Zero to AI Agent, Chapter 16, Section 16.7
# File: orchestrated_system.py

"""
Template for a well-orchestrated multi-agent system.

Features:
- Logging for observability
- Error handling with retries
- Fallback for graceful degradation
- Clean state management
- Clear routing logic
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from datetime import datetime
from dotenv import load_dotenv
import logging

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orchestrator")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)


# =============================================================================
# STATE
# =============================================================================

class OrchestratedState(TypedDict):
    task: str
    stage: str
    result: str
    error: str
    attempts: int
    max_attempts: int


# =============================================================================
# AGENTS WITH ERROR HANDLING
# =============================================================================

def worker_agent(state: OrchestratedState) -> dict:
    """Worker with built-in error handling."""
    logger.info(f"Worker starting (attempt {state.get('attempts', 0) + 1})")
    
    try:
        response = llm.invoke(f"Complete this task briefly: {state['task']}")
        logger.info("Worker completed successfully")
        return {
            "result": response.content,
            "stage": "complete",
            "error": ""
        }
    except Exception as e:
        logger.error(f"Worker failed: {e}")
        return {
            "error": str(e),
            "attempts": state.get("attempts", 0) + 1
        }


def fallback_agent(state: OrchestratedState) -> dict:
    """Fallback when primary worker fails."""
    logger.warning("Using fallback agent")
    return {
        "result": f"Unable to fully complete: {state['task']}. Please try again.",
        "stage": "fallback"
    }


# =============================================================================
# ROUTING
# =============================================================================

def check_result(state: OrchestratedState) -> Literal["done", "retry", "fallback"]:
    """Decide next step based on result."""
    if state.get("result") and not state.get("error"):
        return "done"
    
    attempts = state.get("attempts", 0)
    max_attempts = state.get("max_attempts", 3)
    
    if attempts >= max_attempts:
        return "fallback"
    
    return "retry"


# =============================================================================
# BUILD GRAPH
# =============================================================================

workflow = StateGraph(OrchestratedState)

workflow.add_node("worker", worker_agent)
workflow.add_node("fallback", fallback_agent)

workflow.add_edge(START, "worker")

workflow.add_conditional_edges(
    "worker",
    check_result,
    {
        "done": END,
        "retry": "worker",
        "fallback": "fallback"
    }
)

workflow.add_edge("fallback", END)

app = workflow.compile()


# =============================================================================
# RUN
# =============================================================================

if __name__ == "__main__":
    result = app.invoke({
        "task": "Explain what an API is in one sentence",
        "stage": "starting",
        "result": "",
        "error": "",
        "attempts": 0,
        "max_attempts": 3
    })
    
    print(f"\nResult: {result['result']}")
    print(f"Stage: {result['stage']}")
