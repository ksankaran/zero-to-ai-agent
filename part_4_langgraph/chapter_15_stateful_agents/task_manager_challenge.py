"""
Chapter 15 Challenge: Persistent Task Manager Agent

Build a complete task management agent that demonstrates:
- State schemas with Pydantic validation (15.2)
- State management with reducers (15.3)
- SQLite persistence (15.4)
- Retry logic for external sync (15.5)
- Graceful failure handling (15.6)
- Monitoring and health checks (15.7)

Commands:
- add <title>      : Add a new task
- complete <id>    : Mark task as complete
- list             : Show all tasks
- stats            : Show task statistics
- history          : Show action history
- health           : Run health check
- quit             : Exit (tasks persist!)

Run this file, add some tasks, quit, run again - your tasks should still be there!
"""

from typing import TypedDict, Annotated, Optional
from datetime import datetime
from enum import Enum
from operator import add
import uuid
import time
import random

from pydantic import BaseModel, Field, field_validator
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver


# =============================================================================
# SECTION 1: Enums and Models (15.2 - State Schemas)
# =============================================================================

# TODO: Define TaskStatus enum with values: pending, in_progress, completed, failed
class TaskStatus(str, Enum):
    pass  # Your code here


# TODO: Define TaskPriority enum with values: low, medium, high, urgent
class TaskPriority(str, Enum):
    pass  # Your code here


# TODO: Define Task Pydantic model with validation
# Fields needed: id (str), title (str), description (str), status (TaskStatus), 
#                priority (TaskPriority), created_at (datetime)
# Add a validator that ensures title is not empty
class Task(BaseModel):
    """A task with validation."""
    pass  # Your code here


# =============================================================================
# SECTION 2: State Schema with Reducers (15.3 - State Transformations)
# =============================================================================

# TODO: Define a reducer function for accumulating tasks
# Hint: Should merge existing tasks with new tasks, updating if same ID exists
def task_reducer(existing: list[dict], new: list[dict]) -> list[dict]:
    """Merge task lists, updating existing tasks by ID."""
    pass  # Your code here


# TODO: Define TaskManagerState TypedDict with:
# - tasks: list of task dicts (use Annotated with task_reducer)
# - action_history: list of strings (use Annotated with add for accumulation)
# - last_error: optional string
# - pending_command: optional string
class TaskManagerState(TypedDict):
    pass  # Your code here


# =============================================================================
# SECTION 3: Monitoring (15.7 - Visualization and Monitoring)
# =============================================================================

class TaskMonitor:
    """Track operations and metrics."""
    
    def __init__(self):
        self.operations = []
        self.start_time = datetime.now()
    
    # TODO: Implement log_operation to record operations with timestamps
    def log_operation(self, operation: str, details: str = ""):
        """Log an operation with timestamp."""
        pass  # Your code here
    
    # TODO: Implement get_report to return formatted monitoring report
    def get_report(self) -> str:
        """Get monitoring report."""
        pass  # Your code here


# Global monitor instance
monitor = TaskMonitor()


# =============================================================================
# SECTION 4: Helper Functions
# =============================================================================

def create_task(title: str, description: str = "", priority: str = "medium") -> dict:
    """Create a new task with validation."""
    # TODO: Create and validate a Task using Pydantic, return as dict
    # Handle validation errors gracefully
    pass  # Your code here


def format_task(task: dict) -> str:
    """Format a task for display."""
    status_icons = {
        "pending": "⏳",
        "in_progress": "🔄", 
        "completed": "✅",
        "failed": "❌"
    }
    priority_icons = {
        "low": "🔵",
        "medium": "🟡",
        "high": "🟠",
        "urgent": "🔴"
    }
    
    icon = status_icons.get(task.get("status", "pending"), "❓")
    pri = priority_icons.get(task.get("priority", "medium"), "⚪")
    
    return f"{icon} {pri} [{task['id'][:8]}] {task['title']}"


# =============================================================================
# SECTION 5: Graph Nodes (15.1 - State Management)
# =============================================================================

def parse_command(state: TaskManagerState) -> dict:
    """Parse the pending command and route appropriately."""
    command = state.get("pending_command", "")
    
    # TODO: Parse command and return appropriate routing info
    # Commands: add, complete, list, stats, history, health
    # Return dict with parsed info for next node
    pass  # Your code here


def add_task_node(state: TaskManagerState) -> dict:
    """Add a new task to the state."""
    # TODO: Extract task info from pending_command
    # Create task, log operation, return state update
    # Remember: return {"tasks": [new_task_dict], "action_history": [...]}
    pass  # Your code here


def complete_task_node(state: TaskManagerState) -> dict:
    """Mark a task as completed."""
    # TODO: Find task by ID prefix, update status to completed
    # Handle case where task not found
    # Log operation, return state update
    pass  # Your code here


def list_tasks_node(state: TaskManagerState) -> dict:
    """Display all tasks."""
    tasks = state.get("tasks", [])
    
    if not tasks:
        print("\n📋 No tasks yet! Use 'add <title>' to create one.")
    else:
        print(f"\n📋 Tasks ({len(tasks)}):")
        print("-" * 40)
        for task in tasks:
            print(f"  {format_task(task)}")
    
    return {"action_history": [f"Listed {len(tasks)} tasks"]}


def stats_node(state: TaskManagerState) -> dict:
    """Show task statistics."""
    tasks = state.get("tasks", [])
    
    # TODO: Calculate and display statistics:
    # - Total tasks
    # - Tasks by status (pending, completed, etc.)
    # - Tasks by priority
    pass  # Your code here


def history_node(state: TaskManagerState) -> dict:
    """Show action history."""
    history = state.get("action_history", [])
    
    print(f"\n📜 Action History ({len(history)} actions):")
    print("-" * 40)
    for i, action in enumerate(history[-10:], 1):  # Last 10 actions
        print(f"  {i}. {action}")
    
    return {}


# =============================================================================
# SECTION 6: Retry Logic for External Sync (15.5 - Retry Logic)
# =============================================================================

def sync_tasks_node(state: TaskManagerState) -> dict:
    """
    Simulate syncing tasks to an external service.
    This demonstrates retry logic for transient failures.
    """
    # TODO: Implement retry logic with exponential backoff
    # Simulate a flaky external API (random failures)
    # Use max_retries=3, base_delay=0.5
    # On success: return success message in action_history
    # On failure after retries: return error in last_error, don't crash
    
    max_retries = 3
    base_delay = 0.5
    
    for attempt in range(max_retries):
        try:
            # Simulate flaky API (30% chance of failure)
            if random.random() < 0.3:
                raise ConnectionError("Sync service unavailable")
            
            # Success!
            task_count = len(state.get("tasks", []))
            monitor.log_operation("sync", f"Synced {task_count} tasks")
            print(f"  ✅ Synced {task_count} tasks to cloud")
            return {"action_history": [f"Synced {task_count} tasks successfully"]}
            
        except ConnectionError as e:
            # TODO: Implement exponential backoff with jitter
            # Log the retry attempt
            # If last attempt, handle gracefully (don't crash)
            pass  # Your code here
    
    # All retries failed
    return {
        "last_error": "Sync failed after 3 attempts",
        "action_history": ["Sync failed - will retry later"]
    }


# =============================================================================
# SECTION 7: Health Check (15.7 - Monitoring)
# =============================================================================

def health_check_node(state: TaskManagerState) -> dict:
    """Run health checks on the agent."""
    # TODO: Implement health checks that verify:
    # - State is accessible
    # - No recent errors
    # - Task counts are consistent
    # Print formatted health report
    pass  # Your code here


# =============================================================================
# SECTION 8: Graph Construction
# =============================================================================

def route_command(state: TaskManagerState) -> str:
    """Route to appropriate node based on command."""
    command = state.get("pending_command", "").lower().split()[0] if state.get("pending_command") else ""
    
    routes = {
        "add": "add_task",
        "complete": "complete_task",
        "list": "list_tasks",
        "stats": "stats",
        "history": "history",
        "health": "health_check",
        "sync": "sync_tasks",
    }
    
    return routes.get(command, "list_tasks")


def build_graph() -> StateGraph:
    """Build the task manager graph."""
    # TODO: Create StateGraph with TaskManagerState
    # Add all nodes: add_task, complete_task, list_tasks, stats, history, health_check, sync_tasks
    # Add conditional routing from START based on command
    # All nodes should route to END
    
    builder = StateGraph(TaskManagerState)
    
    # Add nodes
    # builder.add_node("add_task", add_task_node)
    # ... add other nodes
    
    # Add conditional entry point
    # builder.add_conditional_edges(START, route_command, {...})
    
    # Add edges to END
    # builder.add_edge("add_task", END)
    # ... add other edges
    
    pass  # Your code here - return builder.compile(checkpointer=...)


# =============================================================================
# SECTION 9: Main Loop with Persistence (15.4 - Checkpointing)
# =============================================================================

def main():
    """Main entry point with SQLite persistence."""
    print("🗂️  Task Manager Agent")
    print("=" * 40)
    print("Commands: add, complete, list, stats, history, health, sync, quit")
    print("Your tasks persist across restarts!")
    print("=" * 40)
    
    # TODO: Set up SQLite persistence
    # Hint: Use SqliteSaver and pass to graph compilation
    db_path = "task_manager.db"
    
    # TODO: Build graph with checkpointer
    # app = build_graph()
    
    # TODO: Set up config with thread_id for user isolation
    # Support multiple users by changing thread_id
    user_id = input("\nEnter your user ID (or press Enter for 'default'): ").strip() or "default"
    config = {"configurable": {"thread_id": f"user_{user_id}"}}
    
    print(f"\n👤 Logged in as: {user_id}")
    
    # Try to load existing state
    # TODO: Check if user has existing tasks and show count
    
    while True:
        try:
            command = input("\n> ").strip()
            
            if not command:
                continue
            
            if command.lower() == "quit":
                print("\n👋 Goodbye! Your tasks are saved.")
                break
            
            # TODO: Invoke graph with command
            # result = app.invoke({"pending_command": command}, config)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Your tasks are saved.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            monitor.log_operation("error", str(e))


if __name__ == "__main__":
    main()