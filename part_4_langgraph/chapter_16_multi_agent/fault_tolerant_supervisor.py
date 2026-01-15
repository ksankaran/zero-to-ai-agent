# From: Zero to AI Agent, Chapter 16, Section 16.3
# File: fault_tolerant_supervisor.py

"""
Supervisor with error handling and fallbacks.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import random

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


class TaskState(TypedDict):
    task: str
    worker_attempts: int
    max_attempts: int
    result: str
    error: str
    status: str  # "pending", "success", "failed"


def unreliable_worker(state: TaskState) -> dict:
    """A worker that fails 40% of the time (for demonstration)."""
    attempts = state.get("worker_attempts", 0) + 1
    
    # Simulate random failures
    if random.random() < 0.4:
        print(f"❌ Worker failed (attempt {attempts})")
        return {
            "worker_attempts": attempts,
            "error": f"Worker failed on attempt {attempts}",
            "status": "pending"
        }
    
    # Success case
    prompt = f"Complete this task briefly: {state['task']}"
    response = llm.invoke(prompt)
    print(f"✅ Worker succeeded (attempt {attempts})")
    
    return {
        "worker_attempts": attempts,
        "result": response.content,
        "error": "",
        "status": "success"
    }


def fallback_worker(state: TaskState) -> dict:
    """Simpler, more reliable fallback."""
    print("🔄 Fallback worker activated")
    
    prompt = f"Provide a simple response for: {state['task']}"
    response = llm.invoke(prompt)
    
    return {
        "result": f"[Fallback] {response.content}",
        "status": "success"
    }


def supervisor_with_retry(state: TaskState) -> dict:
    """Supervisor that manages retries and fallbacks."""
    attempts = state.get("worker_attempts", 0)
    max_attempts = state.get("max_attempts", 3)
    status = state.get("status", "pending")
    
    if status == "success":
        print("📊 Supervisor: Task completed successfully")
    elif attempts >= max_attempts:
        print(f"📊 Supervisor: Max attempts ({max_attempts}) reached, using fallback")
    else:
        print(f"📊 Supervisor: Attempt {attempts + 1} of {max_attempts}")
    
    return {}  # State already updated by worker


def route_after_attempt(state: TaskState) -> Literal["worker", "fallback", "done"]:
    """Decides next step based on worker result."""
    if state.get("status") == "success":
        return "done"
    
    attempts = state.get("worker_attempts", 0)
    max_attempts = state.get("max_attempts", 3)
    
    if attempts >= max_attempts:
        return "fallback"
    
    return "worker"


# Build the fault-tolerant workflow
workflow = StateGraph(TaskState)

workflow.add_node("supervisor", supervisor_with_retry)
workflow.add_node("worker", unreliable_worker)
workflow.add_node("fallback", fallback_worker)

workflow.add_edge(START, "supervisor")
workflow.add_edge("supervisor", "worker")

# After worker, decide what's next
workflow.add_conditional_edges(
    "worker",
    route_after_attempt,
    {
        "worker": "worker",      # Retry
        "fallback": "fallback",  # Give up, use fallback
        "done": END              # Success!
    }
)

workflow.add_edge("fallback", END)

app = workflow.compile()

# Test reliability
print("Testing fault-tolerant supervisor (results will vary):\n")

for i in range(3):
    print(f"\n{'='*50}")
    print(f"Test run {i+1}")
    print("=" * 50)
    
    result = app.invoke({
        "task": "Explain what Python is in one sentence",
        "worker_attempts": 0,
        "max_attempts": 3,
        "result": "",
        "error": "",
        "status": "pending"
    })
    
    print(f"\nFinal result: {result['result'][:100]}...")
    print(f"Attempts used: {result['worker_attempts']}")
