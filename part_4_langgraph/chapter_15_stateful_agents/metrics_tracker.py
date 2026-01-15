# From: Zero to AI Agent, Chapter 15, Section 15.7
# File: metrics_tracker.py

"""
Track operational metrics for agents.
"""

from collections import defaultdict
from datetime import datetime

class MetricsTracker:
    """Track operational metrics."""
    
    def __init__(self):
        self.counters = defaultdict(int)
        self.timings = defaultdict(list)
        self.errors = []
    
    def increment(self, metric: str, amount: int = 1):
        """Increment a counter."""
        self.counters[metric] += amount
    
    def record_timing(self, operation: str, duration: float):
        """Record how long something took."""
        self.timings[operation].append(duration)
    
    def record_error(self, node: str, error: str):
        """Record an error."""
        self.errors.append({
            "time": datetime.now().isoformat(),
            "node": node,
            "error": error
        })
        self.increment("total_errors")
    
    def summary(self) -> dict:
        """Get metrics summary."""
        timing_stats = {}
        for op, times in self.timings.items():
            timing_stats[op] = {
                "count": len(times),
                "avg": sum(times) / len(times) if times else 0,
                "max": max(times) if times else 0
            }
        
        return {
            "counters": dict(self.counters),
            "timings": timing_stats,
            "error_count": len(self.errors),
            "recent_errors": self.errors[-5:]  # Last 5 errors
        }
    
    def print_summary(self):
        """Print formatted summary."""
        s = self.summary()
        
        print("\n📊 Metrics Summary")
        print("─" * 40)
        
        print("\nCounters:")
        for name, value in s["counters"].items():
            print(f"  {name}: {value}")
        
        print("\nTimings:")
        for op, stats in s["timings"].items():
            print(f"  {op}: avg={stats['avg']:.3f}s, max={stats['max']:.3f}s ({stats['count']} calls)")
        
        if s["recent_errors"]:
            print(f"\nRecent Errors ({s['error_count']} total):")
            for err in s["recent_errors"]:
                print(f"  [{err['node']}] {err['error']}")


# Demo
if __name__ == "__main__":
    import random
    import time
    
    tracker = MetricsTracker()
    
    # Simulate some operations
    print("=== Metrics Tracker Demo ===\n")
    
    for i in range(5):
        # Track API calls
        tracker.increment("api_calls")
        duration = random.uniform(0.1, 0.5)
        tracker.record_timing("api_call", duration)
        
        # Some failures
        if random.random() < 0.3:
            tracker.record_error("api_node", "Connection timeout")
        
        # Track processed items
        tracker.increment("items_processed", random.randint(1, 10))
    
    tracker.print_summary()
