# From: Zero to AI Agent, Chapter 15, Section 15.7
# File: state_monitor.py

"""
Simple state monitoring for LangGraph agents.
"""

from datetime import datetime
from typing import Any

class StateMonitor:
    """Track state changes over time."""
    
    def __init__(self, name: str = "Agent"):
        self.name = name
        self.history = []
        self.start_time = datetime.now()
    
    def record(self, node_name: str, state: dict):
        """Record state after a node runs."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "elapsed": (datetime.now() - self.start_time).total_seconds(),
            "node": node_name,
            "state_snapshot": {k: self._summarize(v) for k, v in state.items()}
        }
        self.history.append(entry)
    
    def _summarize(self, value: Any) -> str:
        """Create a short summary of a value."""
        if isinstance(value, list):
            return f"list[{len(value)}]"
        elif isinstance(value, dict):
            return f"dict[{len(value)}]"
        elif isinstance(value, str) and len(value) > 30:
            return f'"{value[:30]}..."'
        return repr(value)
    
    def report(self):
        """Print a summary report."""
        print(f"\n{'═' * 50}")
        print(f"📈 Monitor Report: {self.name}")
        print(f"{'═' * 50}")
        print(f"Total nodes executed: {len(self.history)}")
        print(f"Total time: {self.history[-1]['elapsed']:.2f}s" if self.history else "N/A")
        
        print(f"\n{'─' * 50}")
        print("Execution Timeline:")
        print(f"{'─' * 50}")
        
        for entry in self.history:
            print(f"  [{entry['elapsed']:5.2f}s] {entry['node']}")
            for key, summary in entry['state_snapshot'].items():
                print(f"           {key}: {summary}")
        
        print(f"{'═' * 50}\n")


def monitored_node(monitor: StateMonitor, original_func, node_name: str):
    """Wrap a node with monitoring."""
    def wrapper(state):
        result = original_func(state)
        # Merge result with state for recording
        new_state = {**state, **result}
        monitor.record(node_name, new_state)
        return result
    return wrapper


def visualize_history(history: list[dict]):
    """Create ASCII timeline of state changes."""
    print("\n📜 State Evolution Timeline")
    print("=" * 60)
    
    for i, snapshot in enumerate(history):
        # Header
        node = snapshot.get("node", f"Step {i}")
        print(f"\n┌─ {node} {'─' * (55 - len(node))}")
        
        # State changes
        state = snapshot.get("state_snapshot", {})
        for key, value in state.items():
            print(f"│  {key}: {value}")
        
        # Connector to next
        if i < len(history) - 1:
            print("│")
            print("▼")
    
    print("\n" + "=" * 60)


# Demo
if __name__ == "__main__":
    monitor = StateMonitor("Demo Agent")
    
    # Simulate some state changes
    monitor.record("start", {"query": "test", "messages": []})
    monitor.record("process", {"query": "test", "messages": ["Hello"], "status": "processing"})
    monitor.record("complete", {"query": "test", "messages": ["Hello", "Done"], "status": "complete"})
    
    monitor.report()
    visualize_history(monitor.history)
