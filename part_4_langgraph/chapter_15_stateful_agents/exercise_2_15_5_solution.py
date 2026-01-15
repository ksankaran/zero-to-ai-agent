# From: Zero to AI Agent, Chapter 15, Section 15.5
# File: exercise_2_15_5_solution.py

"""
Circuit breaker pattern to prevent cascading failures.
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END
from datetime import datetime, timedelta
import time
import random

class CircuitBreaker:
    """
    Circuit breaker with three states:
    - CLOSED: Normal operation, calls go through
    - OPEN: Failing, calls blocked immediately  
    - HALF_OPEN: Testing if service recovered
    """
    
    def __init__(self, failure_threshold: int = 3, reset_timeout: float = 10.0):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.state = "CLOSED"
        self.opened_at = None
    
    def can_execute(self) -> bool:
        """Check if we should attempt the call."""
        if self.state == "CLOSED":
            return True
            
        if self.state == "OPEN":
            # Check if cooldown period has passed
            if datetime.now() - self.opened_at > timedelta(seconds=self.reset_timeout):
                self.state = "HALF_OPEN"
                print(f"  🔄 Circuit HALF_OPEN: Testing service...")
                return True
            return False
            
        # HALF_OPEN: allow one test call
        return True
    
    def record_success(self):
        """Record a successful call."""
        self.failures = 0
        if self.state == "HALF_OPEN":
            print(f"  ✅ Circuit CLOSED: Service recovered!")
        self.state = "CLOSED"
    
    def record_failure(self):
        """Record a failed call."""
        self.failures += 1
        
        if self.state == "HALF_OPEN":
            # Failed during test - reopen
            self.state = "OPEN"
            self.opened_at = datetime.now()
            print(f"  🔴 Circuit OPEN: Test failed, blocking calls")
            
        elif self.failures >= self.failure_threshold:
            self.state = "OPEN"
            self.opened_at = datetime.now()
            print(f"  🔴 Circuit OPEN: {self.failures} failures, blocking calls")

# Global circuit breaker (in real app, would be per-service)
breaker = CircuitBreaker(failure_threshold=3, reset_timeout=5.0)

class BreakerState(TypedDict):
    requests: int
    successes: int
    blocked: int
    log: Annotated[list[str], add]

def call_with_breaker(state: BreakerState) -> dict:
    """Node that uses circuit breaker."""
    if not breaker.can_execute():
        return {
            "blocked": state["blocked"] + 1,
            "log": [f"Request {state['requests'] + 1}: BLOCKED (circuit open)"]
        }
    
    try:
        # Simulate flaky service (80% failure rate)
        if random.random() < 0.8:
            raise ConnectionError("Service failed")
        
        breaker.record_success()
        return {
            "requests": state["requests"] + 1,
            "successes": state["successes"] + 1,
            "log": [f"Request {state['requests'] + 1}: SUCCESS"]
        }
        
    except Exception as e:
        breaker.record_failure()
        return {
            "requests": state["requests"] + 1,
            "log": [f"Request {state['requests'] + 1}: FAILED - {e}"]
        }

# Build graph
graph = StateGraph(BreakerState)
graph.add_node("call", call_with_breaker)
graph.add_edge(START, "call")
graph.add_edge("call", END)
app = graph.compile()

# Demo: Make many requests to see circuit breaker in action
print("=== Circuit Breaker Demo ===\n")

state = {"requests": 0, "successes": 0, "blocked": 0, "log": []}

for i in range(15):
    state = app.invoke(state)
    print(state["log"][-1])
    
    if i == 9:  # Pause to let circuit reset
        print("\n  ⏳ Waiting for circuit reset...\n")
        time.sleep(6)

print(f"\n📊 Summary:")
print(f"  Total requests: {state['requests']}")
print(f"  Successful: {state['successes']}")
print(f"  Blocked: {state['blocked']}")
