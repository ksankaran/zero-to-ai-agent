# From: Zero to AI Agent, Chapter 4, Section 4.7
# other_comprehensions.py - Dictionary and set comprehensions

# Dictionary comprehension
numbers = [1, 2, 3, 4, 5]

# Create a dictionary of squares
squares_dict = {n: n**2 for n in numbers}
print("Squares dict:", squares_dict)
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Word lengths dictionary
words = ["hello", "world", "python"]
word_lengths = {word: len(word) for word in words}
print("Word lengths:", word_lengths)
# {'hello': 5, 'world': 5, 'python': 6}

# Filtering in dictionary comprehension
scores = {"Alice": 85, "Bob": 92, "Charlie": 78, "Diana": 95}
high_scores = {name: score for name, score in scores.items() if score > 90}
print("High scores:", high_scores)
# {'Bob': 92, 'Diana': 95}

# Set comprehension
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]

# Create a set of unique squares
unique_squares = {n**2 for n in numbers}
print("Unique squares:", unique_squares)
# {1, 4, 9, 16}

# Words containing 'a'
words = ["apple", "banana", "cherry", "date"]
words_with_a = {word for word in words if 'a' in word}
print("Words with 'a':", words_with_a)
# {'apple', 'banana', 'date'}
