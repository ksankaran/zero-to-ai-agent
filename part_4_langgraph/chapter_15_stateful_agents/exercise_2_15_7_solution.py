# From: Zero to AI Agent, Chapter 15, Section 15.7
# File: exercise_2_15_7_solution.py

"""
Performance dashboard for agent monitoring.
"""

from collections import defaultdict
from datetime import datetime
import time
import random

class PerformanceDashboard:
    """Track and report node performance."""
    
    def __init__(self):
        self.node_stats = defaultdict(lambda: {
            "calls": 0,
            "successes": 0,
            "failures": 0,
            "total_time": 0.0,
            "times": []
        })
    
    def record(self, node: str, duration: float, success: bool):
        """Record a node execution."""
        stats = self.node_stats[node]
        stats["calls"] += 1
        stats["total_time"] += duration
        stats["times"].append(duration)
        
        if success:
            stats["successes"] += 1
        else:
            stats["failures"] += 1
    
    def wrap_node(self, node_name: str, func):
        """Create a wrapped node that auto-records metrics."""
        def wrapper(state):
            start = time.time()
            success = True
            try:
                result = func(state)
                return result
            except Exception as e:
                success = False
                raise
            finally:
                self.record(node_name, time.time() - start, success)
        return wrapper
    
    def print_report(self):
        """Print formatted performance report."""
        print("\n" + "═" * 60)
        print("📊 PERFORMANCE DASHBOARD")
        print("═" * 60)
        
        # Calculate rankings
        by_time = sorted(
            self.node_stats.items(),
            key=lambda x: x[1]["total_time"],
            reverse=True
        )
        
        print("\n📈 Node Statistics:")
        print("─" * 60)
        print(f"{'Node':<20} {'Calls':>6} {'Avg':>8} {'Total':>8} {'Success':>8}")
        print("─" * 60)
        
        for node, stats in by_time:
            avg = stats["total_time"] / stats["calls"] if stats["calls"] else 0
            rate = stats["successes"] / stats["calls"] * 100 if stats["calls"] else 0
            
            print(f"{node:<20} {stats['calls']:>6} {avg:>7.3f}s {stats['total_time']:>7.3f}s {rate:>7.0f}%")
        
        print("─" * 60)
        
        # Slowest nodes
        print("\n🐢 Slowest Nodes (by avg time):")
        by_avg = sorted(
            self.node_stats.items(),
            key=lambda x: x[1]["total_time"] / max(x[1]["calls"], 1),
            reverse=True
        )[:3]
        
        for i, (node, stats) in enumerate(by_avg, 1):
            avg = stats["total_time"] / stats["calls"]
            print(f"  {i}. {node}: {avg:.3f}s avg")
        
        print("\n" + "═" * 60)

# Demo
if __name__ == "__main__":
    dashboard = PerformanceDashboard()
    
    # Simulate some runs
    print("=== Performance Dashboard Demo ===")
    print("Simulating 10 agent runs...\n")
    
    for _ in range(10):
        dashboard.record("fetch_data", random.uniform(0.1, 0.5), random.random() > 0.1)
        dashboard.record("process", random.uniform(0.2, 0.8), random.random() > 0.2)
        dashboard.record("save", random.uniform(0.05, 0.15), random.random() > 0.05)
    
    dashboard.print_report()
