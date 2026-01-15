# From: Zero to AI Agent, Chapter 5, Section 5.3
# File: multiple_values.py

def get_min_max(numbers):
    """Return both minimum and maximum from a list"""
    return min(numbers), max(numbers)  # Return TWO values!

# Get both values
scores = [85, 92, 78, 95, 88]
lowest, highest = get_min_max(scores)
print(f"Lowest: {lowest}, Highest: {highest}")

# You can also capture them as a tuple
result = get_min_max(scores)
print(f"Result tuple: {result}")