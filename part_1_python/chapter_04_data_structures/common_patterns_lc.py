# From: Zero to AI Agent, Chapter 4, Section 4.7
# common_patterns.py - Common patterns and recipes

# Pattern 1: Flatten a list of lists
nested = [[1, 2], [3, 4], [5, 6]]
flat = [item for sublist in nested for item in sublist]
print("Flattened:", flat)  # [1, 2, 3, 4, 5, 6]

# Pattern 2: Remove None values
data = [1, None, 2, None, 3, 4, None, 5]
clean = [x for x in data if x is not None]
print("Without None:", clean)  # [1, 2, 3, 4, 5]

# Pattern 3: Extract from nested structures
data = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 92},
    {"name": "Charlie", "score": 78}
]
passing = [d["name"] for d in data if d["score"] >= 80]
print("Passing students:", passing)  # ['Alice', 'Bob']

# Pattern 4: Create enumerated pairs
items = ["a", "b", "c"]
enumerated = [(i, item) for i, item in enumerate(items)]
print("Enumerated:", enumerated)  # [(0, 'a'), (1, 'b'), (2, 'c')]

# Pattern 5: Zip multiple lists
names = ["Alice", "Bob", "Charlie"]
ages = [30, 25, 35]
combined = [(name, age) for name, age in zip(names, ages)]
print("Combined:", combined)  # [('Alice', 30), ('Bob', 25), ('Charlie', 35)]

# Pattern 6: String operations
sentences = ["Hello world", "Python programming", "AI is cool"]
word_counts = [len(s.split()) for s in sentences]
print("Word counts:", word_counts)  # [2, 2, 3]

# Pattern 7: Working with ranges
# Even numbers from 0 to 20
evens = [x for x in range(21) if x % 2 == 0]
print("Evens:", evens)

# Squares of numbers from 1 to 10
squares = [x**2 for x in range(1, 11)]
print("Squares:", squares)
