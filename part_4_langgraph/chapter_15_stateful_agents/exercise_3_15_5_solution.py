# From: Zero to AI Agent, Chapter 15, Section 15.5
# File: exercise_3_15_5_solution.py

"""
Simple retry monitoring dashboard.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END
import random

@dataclass
class RetryStats:
    """Statistics for a single node."""
    total_calls: int = 0
    successful_calls: int = 0
    total_retries: int = 0
    
    @property
    def failure_rate(self) -> float:
        if self.total_calls == 0:
            return 0.0
        return 1 - (self.successful_calls / self.total_calls)
    
    @property
    def avg_retries_per_success(self) -> float:
        if self.successful_calls == 0:
            return 0.0
        return self.total_retries / self.successful_calls

class RetryDashboard:
    """Central monitoring for retry behavior."""
    
    def __init__(self, alert_threshold: float = 0.5):
        self.stats: dict[str, RetryStats] = {}
        self.alert_threshold = alert_threshold
    
    def record(self, node_name: str, success: bool, retries: int):
        """Record an operation result."""
        if node_name not in self.stats:
            self.stats[node_name] = RetryStats()
        
        stats = self.stats[node_name]
        stats.total_calls += 1
        stats.total_retries += retries
        if success:
            stats.successful_calls += 1
        
        # Check for alert condition
        if stats.failure_rate > self.alert_threshold and stats.total_calls >= 5:
            print(f"  ⚠️ ALERT: {node_name} failure rate is {stats.failure_rate:.0%}!")
    
    def report(self):
        """Print dashboard report."""
        print("\n" + "=" * 50)
        print("📊 RETRY DASHBOARD")
        print("=" * 50)
        
        for name, stats in self.stats.items():
            print(f"\n📌 {name}:")
            print(f"   Calls: {stats.total_calls}")
            print(f"   Success rate: {(1 - stats.failure_rate):.0%}")
            print(f"   Total retries: {stats.total_retries}")
            print(f"   Avg retries/success: {stats.avg_retries_per_success:.1f}")
        
        print("\n" + "=" * 50)

# Global dashboard
dashboard = RetryDashboard(alert_threshold=0.4)

# Nodes that report to dashboard
def node_a(state: dict) -> dict:
    """Mostly reliable node."""
    retries = 0
    success = random.random() > 0.2  # 80% success
    
    if not success:
        retries = random.randint(1, 3)
        
    dashboard.record("node_a", success, retries)
    return {"a_done": True}

def node_b(state: dict) -> dict:
    """Less reliable node."""
    retries = 0
    success = random.random() > 0.5  # 50% success
    
    if not success:
        retries = random.randint(2, 5)
        
    dashboard.record("node_b", success, retries)
    return {"b_done": True}

def node_c(state: dict) -> dict:
    """Unreliable node - will trigger alerts."""
    retries = 0
    success = random.random() > 0.7  # Only 30% success
    
    if not success:
        retries = random.randint(3, 5)
        
    dashboard.record("node_c", success, retries)
    return {"c_done": True}

# Build graph
class DashState(TypedDict):
    a_done: bool
    b_done: bool
    c_done: bool

graph = StateGraph(DashState)
graph.add_node("a", node_a)
graph.add_node("b", node_b)
graph.add_node("c", node_c)
graph.add_edge(START, "a")
graph.add_edge("a", "b")
graph.add_edge("b", "c")
graph.add_edge("c", END)
app = graph.compile()

# Run multiple times
print("=== Retry Dashboard Demo ===\n")

for i in range(10):
    print(f"Run {i + 1}...")
    app.invoke({"a_done": False, "b_done": False, "c_done": False})

# Show report
dashboard.report()
