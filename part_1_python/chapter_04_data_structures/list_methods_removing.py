# From: Zero to AI Agent, Chapter 4, Section 4.2
# list_methods_removing.py - Methods for removing items from lists

# Let's work with a list of tasks
tasks = ["email client", "fix bug", "write tests", "fix bug", "deploy", "fix bug"]
print("Original tasks:", tasks)

# Method 1: remove() - Removes the FIRST occurrence of a value
tasks.remove("fix bug")  # Only removes the first "fix bug"
print("After remove('fix bug'):", tasks)

# Method 2: pop() - Removes and RETURNS an item at a specific index
completed_task = tasks.pop()  # No index = removes last item
print(f"Completed: {completed_task}")
print("Tasks after pop():", tasks)

first_task = tasks.pop(0)  # Remove and return first item
print(f"Did first: {first_task}")
print("Tasks after pop(0):", tasks)

# Method 3: clear() - Removes ALL items
old_tasks = ["outdated task 1", "outdated task 2"]
print(f"Old tasks before clear: {old_tasks}")
old_tasks.clear()
print(f"Old tasks after clear: {old_tasks}")

# Method 4: del - Not a method, but a statement (be careful with this one!)
numbers = [1, 2, 3, 4, 5]
del numbers[2]  # Removes the item at index 2
print("After del numbers[2]:", numbers)

# You can also delete slices!
del numbers[1:3]  # Removes items at index 1 and 2
print("After del numbers[1:3]:", numbers)
