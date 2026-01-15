# From: Building AI Agents, Chapter 14, Section 14.7
# File: exercise_3_14_7_solution.py

"""Debug dashboard for analyzing LangGraph executions.

Exercise 3 Solution: Build a debug dashboard that produces:
- Total nodes visited
- Time spent
- State changes for each field
- Fields that never changed
- Routing decisions made
"""

from datetime import datetime
from collections import defaultdict


class DebugDashboard:
    """Comprehensive execution analysis dashboard."""
    
    def __init__(self):
        self.executions = []
        self.current_execution = None
    
    def start_execution(self, name: str = None):
        """Start tracking a new execution."""
        self.current_execution = {
            "name": name or f"Execution_{len(self.executions) + 1}",
            "started": datetime.now(),
            "ended": None,
            "steps": [],
            "routing_decisions": [],
            "initial_state": None,
            "final_state": None
        }
    
    def record_step(self, node_name: str, state_before: dict, updates: dict):
        """Record a single step in the execution."""
        if not self.current_execution:
            self.start_execution()
        
        step = {
            "timestamp": datetime.now(),
            "node": node_name,
            "state_before": dict(state_before),
            "updates": dict(updates) if updates else {}
        }
        self.current_execution["steps"].append(step)
        
        # Track initial state
        if self.current_execution["initial_state"] is None:
            self.current_execution["initial_state"] = dict(state_before)
    
    def record_routing(self, router_name: str, decision: str, reason: str = None):
        """Record a routing decision."""
        if self.current_execution:
            self.current_execution["routing_decisions"].append({
                "timestamp": datetime.now(),
                "router": router_name,
                "decision": decision,
                "reason": reason
            })
    
    def end_execution(self, final_state: dict):
        """End the current execution."""
        if self.current_execution:
            self.current_execution["ended"] = datetime.now()
            self.current_execution["final_state"] = dict(final_state)
            self.executions.append(self.current_execution)
            self.current_execution = None
    
    def generate_report(self, execution_index: int = -1) -> str:
        """Generate a comprehensive report for an execution."""
        if not self.executions:
            return "No executions recorded."
        
        exec_data = self.executions[execution_index]
        
        lines = []
        lines.append("=" * 60)
        lines.append(f"📊 DEBUG REPORT: {exec_data['name']}")
        lines.append("=" * 60)
        
        # Timing
        duration = (exec_data['ended'] - exec_data['started']).total_seconds()
        lines.append(f"\n⏱️  TIMING")
        lines.append(f"   Started: {exec_data['started'].strftime('%H:%M:%S.%f')[:-3]}")
        lines.append(f"   Ended: {exec_data['ended'].strftime('%H:%M:%S.%f')[:-3]}")
        lines.append(f"   Duration: {duration:.3f} seconds")
        
        # Node visits
        lines.append(f"\n📍 NODE VISITS ({len(exec_data['steps'])} total)")
        node_counts = defaultdict(int)
        for step in exec_data['steps']:
            node_counts[step['node']] += 1
        for node, count in node_counts.items():
            marker = "⚠️ " if count > 1 else "   "
            lines.append(f"{marker}{node}: {count} visit(s)")
        
        # Routing decisions
        lines.append(f"\n🔀 ROUTING DECISIONS ({len(exec_data['routing_decisions'])})")
        for rd in exec_data['routing_decisions']:
            reason = f" ({rd['reason']})" if rd['reason'] else ""
            lines.append(f"   {rd['router']} → {rd['decision']}{reason}")
        
        # State changes
        lines.append(f"\n📝 STATE CHANGES")
        all_fields = set()
        for step in exec_data['steps']:
            all_fields.update(step['state_before'].keys())
            all_fields.update(step['updates'].keys())
        
        initial = exec_data['initial_state'] or {}
        final = exec_data['final_state'] or {}
        
        for field in sorted(all_fields):
            initial_val = initial.get(field, "<not set>")
            final_val = final.get(field, "<not set>")
            
            # Truncate long values
            iv_str = str(initial_val)[:30]
            fv_str = str(final_val)[:30]
            
            if initial_val == final_val:
                lines.append(f"   {field}: {fv_str} (unchanged)")
            else:
                lines.append(f"   {field}: {iv_str} → {fv_str}")
        
        # Fields that never changed
        unchanged = []
        for field in all_fields:
            if initial.get(field) == final.get(field) and field in initial:
                unchanged.append(field)
        
        if unchanged:
            lines.append(f"\n⚠️  NEVER CHANGED: {', '.join(unchanged)}")
        
        lines.append("\n" + "=" * 60)
        
        return "\n".join(lines)


# === EXAMPLE USAGE ===

def example_usage():
    """Demonstrate the dashboard."""
    dashboard = DebugDashboard()
    
    # Simulate an execution
    dashboard.start_execution("Test Run")
    
    state = {"query": "test", "results": [], "count": 0}
    
    dashboard.record_step("search", state, {"results": ["r1"], "count": 1})
    dashboard.record_routing("should_continue", "continue", "count < max")
    
    state = {"query": "test", "results": ["r1"], "count": 1}
    dashboard.record_step("search", state, {"results": ["r2"], "count": 2})
    dashboard.record_routing("should_continue", "done", "count >= max")
    
    final = {"query": "test", "results": ["r1", "r2"], "count": 2}
    dashboard.end_execution(final)
    
    print(dashboard.generate_report())


if __name__ == "__main__":
    example_usage()


# === HOW TO USE IN YOUR GRAPH ===
"""
from debug_dashboard import DebugDashboard

dashboard = DebugDashboard()

def my_node(state: MyState) -> dict:
    # ... your logic ...
    updates = {"field": "value"}
    
    dashboard.record_step("my_node", state, updates)
    return updates

def my_router(state: MyState) -> str:
    decision = "some_path"
    dashboard.record_routing("my_router", decision, f"score={state.get('score')}")
    return decision

# In main:
dashboard.start_execution("My Test")
result = app.invoke(initial_state)
dashboard.end_execution(result)
print(dashboard.generate_report())
"""
