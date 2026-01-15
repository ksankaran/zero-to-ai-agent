# From: Zero to AI Agent, Chapter 5, Section 5.5
# File: lambda_filtering_pattern.py

# 2. FILTERING - Keep only items that match criteria
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Keep only even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Even numbers: {evens}")  # [2, 4, 6, 8, 10]

# Keep only numbers greater than 5
big_numbers = list(filter(lambda x: x > 5, numbers))
print(f"Numbers > 5: {big_numbers}")  # [6, 7, 8, 9, 10]