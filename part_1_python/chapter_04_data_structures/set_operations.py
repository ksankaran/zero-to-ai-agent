# From: Zero to AI Agent, Chapter 4, Section 4.5
# set_operations.py - Basic set operations: add, remove, check

# Working with a set of skills for an AI developer
skills = {"Python", "Machine Learning", "Data Analysis"}
print(f"Initial skills: {skills}")

# Adding elements
skills.add("Deep Learning")
skills.add("Python")  # Try to add duplicate - nothing happens!
print(f"After adding: {skills}")

# Adding multiple elements
new_skills = ["Statistics", "SQL", "Cloud Computing", "SQL"]  # Note: SQL appears twice
skills.update(new_skills)  # Adds all unique elements
print(f"After update: {skills}")

# Removing elements - different methods
skills.remove("SQL")  # Removes SQL (raises error if not found)
print(f"After remove: {skills}")

# Safe removal with discard (no error if not found)
skills.discard("JavaScript")  # Not in set, but no error
skills.discard("Statistics")  # Removes if present
print(f"After discard: {skills}")

# Pop removes and returns an arbitrary element
if skills:  # Check if not empty
    popped = skills.pop()
    print(f"Popped: {popped}")
    print(f"Remaining: {skills}")

# Checking membership (SUPER FAST!)
ai_skills = {"Python", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas"}

# This is incredibly fast even with huge sets
if "Python" in ai_skills:
    print("Python is in the skill set")

if "Java" not in ai_skills:
    print("Java is not in the skill set")

# Length and clearing
print(f"Number of skills: {len(ai_skills)}")
# ai_skills.clear()  # Removes all elements
