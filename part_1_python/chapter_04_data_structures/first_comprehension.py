# From: Zero to AI Agent, Chapter 4, Section 4.7
# first_comprehension.py - Your first list comprehension

# The way you know - using a loop
squares_loop = []
for x in range(5):
    squares_loop.append(x ** 2)
print("Using loop:", squares_loop)

# The SAME thing using a list comprehension
squares_comp = [x ** 2 for x in range(5)]
print("Using comprehension:", squares_comp)

# They produce the exact same result!
# [0, 1, 4, 9, 16]

# Anatomy of a list comprehension:
# [expression for item in iterable]
#  ↑          ↑        ↑
#  │          │        └── Where the items come from (range, list, etc.)
#  │          └──────────── Variable name for each item
#  └──────────────────────── What to do with each item

# More examples to build intuition
numbers = [1, 2, 3, 4, 5]

# Double each number
doubled = [n * 2 for n in numbers]
print("Doubled:", doubled)  # [2, 4, 6, 8, 10]

# Convert to strings
strings = [str(n) for n in numbers]
print("As strings:", strings)  # ['1', '2', '3', '4', '5']

# Create a list of lengths
words = ["hi", "hello", "python", "ai"]
lengths = [len(word) for word in words]
print("Word lengths:", lengths)  # [2, 5, 6, 2]
