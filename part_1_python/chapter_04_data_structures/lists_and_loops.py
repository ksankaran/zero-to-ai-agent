# From: Zero to AI Agent, Chapter 4, Section 4.1
# lists_and_loops.py - Combining lists with loops from Chapter 3

# Using loops with lists (building on Chapter 3!)
scores = [85, 92, 78, 95, 88, 73, 91]

# For loop through a list (remember this pattern?)
print("All scores:")
for score in scores:
    print(f"  Score: {score}")

# Using enumerate to get both index and value
print("\nScores with position:")
for position, score in enumerate(scores):
    print(f"  Position {position}: {score}")

# Using conditions with lists (Chapter 3 skills!)
print("\nHigh scores (90+):")
for score in scores:
    if score >= 90:  # Our if statement from Chapter 3!
        print(f"  Excellent: {score}")

# Accessing by index with a loop
print("\nFirst half of scores:")
for i in range(len(scores) // 2):  # Using range from Chapter 3
    print(f"  scores[{i}] = {scores[i]}")
