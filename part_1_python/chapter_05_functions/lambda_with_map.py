# From: Zero to AI Agent, Chapter 5, Section 5.5
# File: lambda_with_map.py

# Say we have a list of numbers
numbers = [1, 2, 3, 4, 5]

# We want to apply a function to each number
# Without lambda - need to define a function first
def square(x):
    return x ** 2

squared = list(map(square, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# With lambda - do it all in one line!
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]