# From: Zero to AI Agent, Chapter 15, Section 15.5
# File: resilient_node.py

"""
A complete example of a resilient LangGraph node.
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import random
import time

class TaskState(TypedDict):
    task: str
    result: str
    status: str
    attempt_log: Annotated[list[str], add]

def resilient_processor(state: TaskState) -> dict:
    """
    A node with built-in retry logic.
    
    This demonstrates the pattern without external decorators,
    so you can see exactly what's happening.
    """
    max_attempts = 3
    base_delay = 1.0
    
    for attempt in range(max_attempts):
        try:
            # Simulate flaky operation (fails 60% of time)
            if random.random() < 0.6:
                raise ConnectionError("Simulated failure")
            
            # Success!
            return {
                "result": f"Processed: {state['task']}",
                "status": "success",
                "attempt_log": [f"Attempt {attempt + 1}: Success ✓"]
            }
            
        except ConnectionError as e:
            log_entry = f"Attempt {attempt + 1}: Failed - {e}"
            
            if attempt < max_attempts - 1:
                wait = base_delay * (2 ** attempt)
                log_entry += f" (retrying in {wait}s)"
                time.sleep(wait)
            
            if attempt == max_attempts - 1:
                # Final attempt failed
                return {
                    "result": "",
                    "status": "failed",
                    "attempt_log": [log_entry + " - giving up"]
                }
            
            # Will retry - just log this attempt
            # (The loop continues, so we don't return yet)

# Build and test
graph = StateGraph(TaskState)
graph.add_node("process", resilient_processor)
graph.add_edge(START, "process")
graph.add_edge("process", END)

app = graph.compile(checkpointer=MemorySaver())

# Run multiple times to see retry behavior
print("=== Resilient Node Demo ===\n")

for i in range(3):
    config = {"configurable": {"thread_id": f"test-{i}"}}
    result = app.invoke({
        "task": f"Task #{i + 1}",
        "result": "",
        "status": "pending",
        "attempt_log": []
    }, config)
    
    print(f"Task #{i + 1}: {result['status']}")
    for log in result['attempt_log']:
        print(f"  {log}")
    print()
