# From: Zero to AI Agent, Chapter 12, Section 12.4
# File: exercise_3_12_4_solution.py

from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Simple task storage
tasks = {}
task_id = 0

class AddTaskInput(BaseModel):
    title: str = Field(description="Task title")
    priority: Literal["low", "medium", "high"] = Field(default="medium")
    due_date: Optional[str] = Field(default=None, description="Due date YYYY-MM-DD")

class ListTasksInput(BaseModel):
    filter_by: str = Field(default="all", description="Filter by: all, priority, or date")

class CompleteTaskInput(BaseModel):
    task_id: int = Field(description="Task ID number to mark complete")

def add_task(title: str, priority: str = "medium", due_date: str = None) -> str:
    """Add a new task."""
    global task_id
    task_id += 1
    
    # Parse due date
    if due_date:
        try:
            due = datetime.strptime(due_date, "%Y-%m-%d")
        except:
            return f"Error: Invalid date format. Use YYYY-MM-DD"
    else:
        due = None
    
    tasks[task_id] = {
        "title": title,
        "priority": priority,
        "due_date": due_date,
        "status": "pending"
    }
    return f"Task #{task_id} added: '{title}' [{priority}]"

def list_tasks(filter_by: str = "all") -> str:
    """List tasks filtered by: all, priority, or date."""
    if not tasks:
        return "No tasks"
    
    if filter_by == "priority":
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_tasks = sorted(
            tasks.items(),
            key=lambda x: priority_order.get(x[1]["priority"], 3)
        )
    else:
        sorted_tasks = list(tasks.items())
    
    result = []
    for tid, task in sorted_tasks:
        status = "✓" if task["status"] == "complete" else "•"
        result.append(f"{status} Task #{tid}: {task['title']} [{task['priority']}]")
    
    return "\n".join(result)

def complete_task(task_id: int) -> str:
    """Mark a task as complete."""
    if task_id not in tasks:
        return f"Error: Task #{task_id} not found"
    tasks[task_id]["status"] = "complete"
    return f"Task #{task_id} marked complete"

# Create tools with proper args_schema
tools = [
    Tool.from_function(
        func=add_task,
        name="AddTask",
        description="Add a new task",
        args_schema=AddTaskInput
    ),
    Tool.from_function(
        func=list_tasks,
        name="ListTasks",
        description="List all tasks",
        args_schema=ListTasksInput
    ),
    Tool.from_function(
        func=complete_task,
        name="CompleteTask",
        description="Mark task complete",
        args_schema=CompleteTaskInput
    )
]

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# Test commands
commands = [
    "Add a high priority task to call mom tomorrow",
    "Add task: Review report (low priority)",
    "List all tasks",
    "Mark task 1 as complete"
]

for cmd in commands:
    print(f"\n➤ {cmd}")
    response = llm_with_tools.invoke([HumanMessage(content=cmd)])
    
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        # Execute the tool
        if tool_call['name'] == 'AddTask':
            result = add_task(**tool_call['args'])
        elif tool_call['name'] == 'ListTasks':
            result = list_tasks(**tool_call['args'])
        elif tool_call['name'] == 'CompleteTask':
            result = complete_task(**tool_call['args'])
        print(result)