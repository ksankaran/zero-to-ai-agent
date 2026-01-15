# From: Zero to AI Agent, Chapter 4, Section 4.7
# Exercise 1: Data Cleaning

# Original messy data
messy_data = ["  hello  ", " WORLD ", "  Python  "]

# Create cleaned list: stripped and lowercase
cleaned = [s.strip().lower() for s in messy_data]
print(f"Cleaned data: {cleaned}")

# Filter out strings shorter than 4 characters
filtered = [s.strip().lower() for s in messy_data if len(s.strip()) >= 4]
print(f"Filtered (>= 4 chars): {filtered}")

# Combined: clean and filter in one comprehension
final = [s.strip().lower() for s in messy_data if len(s.strip()) >= 4]
print(f"Final result: {final}")
