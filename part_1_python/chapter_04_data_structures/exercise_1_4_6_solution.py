# From: Zero to AI Agent, Chapter 4, Section 4.6
# Exercise 1: Task Management System

# Store tasks with different structures
# Individual tasks - LIST OF DICTIONARIES (ordered, need all fields)
tasks = [
    {"id": 1, "title": "Review code", "priority": "high", "status": "pending"},
    {"id": 2, "title": "Write tests", "priority": "medium", "status": "in_progress"},
    {"id": 3, "title": "Deploy app", "priority": "high", "status": "pending"}
]

# Unique tags - SET (no duplicates)
all_tags = {"coding", "testing", "deployment", "review"}

# Quick lookup by ID - DICTIONARY
task_lookup = {task["id"]: task for task in tasks}

# Group by status - DICTIONARY OF LISTS
tasks_by_status = {}
for task in tasks:
    status = task["status"]
    if status not in tasks_by_status:
        tasks_by_status[status] = []
    tasks_by_status[status].append(task)

print("Tasks by status:", tasks_by_status)
print(f"All unique tags: {all_tags}")
print(f"Quick lookup task 2: {task_lookup[2]['title']}")
