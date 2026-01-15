# From: Zero to AI Agent, Chapter 4, Section 4.7
# writing_tips.py - Tips for writing good comprehensions

# Good examples:
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
words = ["hello", "world", "python", "programming", "ai"]
people = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 17},
    {"name": "Charlie", "age": 30}
]

# 1. Keep them simple
squares = [x**2 for x in range(10)]
print("Simple squares:", squares[:5])

# 2. Clear variable names
uppercase = [word.upper() for word in words]
print("Uppercase words:", uppercase[:3])

# 3. Readable conditions
adults = [person for person in people if person["age"] >= 18]
print("Adults:", [p["name"] for p in adults])

# Bad examples (too complex):
# Don't do this - too hard to read:
# result = [[y for y in row if y > 0] for row in matrix if sum(row) > 10]

# When in doubt, write the loop first, then convert:
print("\nLoop to comprehension conversion:")

# Step 1: Write the loop
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result_loop = []
for x in data:
    if x % 2 == 0:
        result_loop.append(x * 2)
print("Loop result:", result_loop)

# Step 2: Convert to comprehension
result_comp = [x * 2 for x in data if x % 2 == 0]
print("Comprehension result:", result_comp)

print("\nRemember:")
print("1. Keep them simple - If you need to read it twice, it's too complex")
print("2. One line only - If it wraps to multiple lines, use a regular loop")
print("3. Clear variable names - Use 'word' not 'w', 'number' not 'n'")
print("4. Don't sacrifice readability - Shorter isn't always better")
print("5. Use them for building, not printing - They create lists, not side effects")
