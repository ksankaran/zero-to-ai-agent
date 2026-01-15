# From: Zero to AI Agent, Chapter 5, Section 5.5
# File: exercise_1_5_5_solution.py

numbers = [1, -2, 3, -4, 5, -6, 7]
words = ["python", "lambda", "function"]

# 1. Square all numbers
squared = list(map(lambda x: x ** 2, numbers))
print(f"Squared: {squared}")  # [1, 4, 9, 16, 25, 36, 49]

# 2. Filter out negative numbers
positives = list(filter(lambda x: x > 0, numbers))
print(f"Positive numbers: {positives}")  # [1, 3, 5, 7]

# 3. Convert strings to uppercase
uppercase = list(map(lambda word: word.upper(), words))
print(f"Uppercase: {uppercase}")  # ['PYTHON', 'LAMBDA', 'FUNCTION']

# Bonus: Combine operations - square only positive numbers
positive_squares = list(map(lambda x: x ** 2, 
                           filter(lambda x: x > 0, numbers)))
print(f"Squares of positives: {positive_squares}")  # [1, 9, 25, 49]