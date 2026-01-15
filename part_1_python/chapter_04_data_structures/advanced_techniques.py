# From: Zero to AI Agent, Chapter 4, Section 4.4
# advanced_techniques.py - Advanced dictionary techniques

# Merging dictionaries
defaults = {"color": "blue", "size": "medium", "quantity": 1}
user_choices = {"color": "red", "quantity": 3}

# Merge (user choices override defaults)
final = {**defaults, **user_choices}
print(f"Final options: {final}")

# Dictionary comprehensions
# Square numbers
squares = {n: n**2 for n in range(1, 6)}
print(f"\nSquares: {squares}")

# Filter a dictionary
scores = {"Alice": 85, "Bob": 92, "Charlie": 78, "Diana": 95}
high_scores = {name: score for name, score in scores.items() if score >= 90}
print(f"High scores: {high_scores}")

# Invert a dictionary (swap keys and values)
color_codes = {"red": "#FF0000", "green": "#00FF00", "blue": "#0000FF"}
code_to_color = {code: color for color, code in color_codes.items()}
print(f"Inverted: {code_to_color}")

# Grouping data
students = [
    {"name": "Alice", "grade": "A"},
    {"name": "Bob", "grade": "B"},
    {"name": "Charlie", "grade": "A"},
    {"name": "Diana", "grade": "B"},
    {"name": "Eve", "grade": "A"}
]

# Group by grade
by_grade = {}
for student in students:
    grade = student["grade"]
    if grade not in by_grade:
        by_grade[grade] = []
    by_grade[grade].append(student["name"])

print("\nStudents by grade:")
for grade, names in by_grade.items():
    print(f"  Grade {grade}: {names}")

# Word frequency counter
text = "the quick brown fox jumps over the lazy dog the fox"
word_counter = {}

for word in text.split():
    if word in word_counter:
        word_counter[word] += 1
    else:
        word_counter[word] = 1

print("\nWord frequencies:")
for word, count in word_counter.items():
    print(f"  {word}: {count}")
