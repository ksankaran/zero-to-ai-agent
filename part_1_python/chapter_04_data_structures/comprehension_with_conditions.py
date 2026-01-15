# From: Zero to AI Agent, Chapter 4, Section 4.7
# comprehension_with_conditions.py - Adding conditions to filter lists

# The loop way you know
evens_loop = []
for x in range(10):
    if x % 2 == 0:
        evens_loop.append(x)
print("Evens (loop):", evens_loop)

# The comprehension way with a condition
evens_comp = [x for x in range(10) if x % 2 == 0]
print("Evens (comprehension):", evens_comp)

# Both give: [0, 2, 4, 6, 8]

# The pattern with conditions:
# [expression for item in iterable if condition]
#  ↑          ↑        ↑           ↑
#  │          │        │           └── Only include if this is True
#  │          │        └──────────────── Where items come from
#  │          └────────────────────────── Variable for each item
#  └────────────────────────────────────── What to do with item

# More examples with conditions
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Only positive numbers
positives = [n for n in numbers if n > 0]
print("Positives:", positives)

# Only numbers greater than 5
big_numbers = [n for n in numbers if n > 5]
print("Greater than 5:", big_numbers)  # [6, 7, 8, 9, 10]

# Squares of only even numbers
even_squares = [n ** 2 for n in numbers if n % 2 == 0]
print("Squares of evens:", even_squares)  # [4, 16, 36, 64, 100]

# Words that are longer than 3 characters
words = ["hi", "hello", "python", "ai", "code"]
long_words = [word for word in words if len(word) > 3]
print("Long words:", long_words)  # ['hello', 'python', 'code']
