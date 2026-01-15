# From: Building AI Agents, Chapter 14, Section 14.7
# File: state_tracker.py

"""Track state changes through graph execution.

Captures the full state at each node for later analysis.
Useful for debugging complex state transformations.
"""

import copy
from datetime import datetime


class StateTracker:
    """Captures state at each node for later analysis."""
    
    def __init__(self):
        self.history = []
    
    def capture(self, node_name: str, state: dict, updates: dict = None):
        """Record state at a point in execution.
        
        Args:
            node_name: Name of the current node
            state: The state dictionary before updates
            updates: The updates being returned (optional)
        """
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "node": node_name,
            "state_before": copy.deepcopy(dict(state)),
            "updates": copy.deepcopy(updates) if updates else None
        }
        self.history.append(snapshot)
    
    def print_history(self):
        """Print the execution history."""
        print("\n" + "=" * 60)
        print("📜 EXECUTION HISTORY")
        print("=" * 60)
        
        for i, snapshot in enumerate(self.history):
            print(f"\n--- Step {i + 1}: {snapshot['node']} ---")
            print(f"Time: {snapshot['timestamp']}")
            
            if snapshot['updates']:
                print("Updates made:")
                for key, value in snapshot['updates'].items():
                    print(f"  {key}: {value}")
    
    def find_changes(self, field: str):
        """Track how a specific field changed over time.
        
        Args:
            field: The state field to track
        """
        print(f"\n📊 History of '{field}':")
        
        for snapshot in self.history:
            value = snapshot['state_before'].get(field, '<not set>')
            update = snapshot['updates'].get(field, '<no change>') if snapshot['updates'] else '<no change>'
            print(f"  {snapshot['node']}: {value} → {update}")
    
    def clear(self):
        """Reset the history."""
        self.history = []


# Global tracker instance for easy import
tracker = StateTracker()


# Example usage
if __name__ == "__main__":
    # Simulate some node executions
    tracker.capture("node_1", {"count": 0, "status": "starting"}, {"count": 1})
    tracker.capture("node_2", {"count": 1, "status": "starting"}, {"status": "processing"})
    tracker.capture("node_3", {"count": 1, "status": "processing"}, {"count": 2, "status": "done"})
    
    # Show the history
    tracker.print_history()
    
    # Track a specific field
    tracker.find_changes("count")
    tracker.find_changes("status")
