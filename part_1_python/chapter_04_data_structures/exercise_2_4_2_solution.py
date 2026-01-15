# From: Zero to AI Agent, Chapter 4, Section 4.2
# Exercise 2: Score Tracker

# 1. Start with initial scores
scores = [75, 82, 90, 68, 95, 78]
print("Initial scores:", scores)

# 2. Add three more scores using extend()
new_scores = [88, 92, 79]
scores.extend(new_scores)
print("After adding new scores:", scores)

# 3. Find highest and lowest
highest = max(scores)
lowest = min(scores)
print(f"Highest: {highest}, Lowest: {lowest}")

# 4. Calculate average
average = sum(scores) / len(scores)
print(f"Average score: {average:.2f}")

# 5. Remove lowest score
scores.remove(lowest)
print("After removing lowest:", scores)

# 6. Sort from highest to lowest
scores.sort(reverse=True)
print("Sorted (high to low):", scores)

# 7. Display top 3
top_3 = scores[:3]
print(f"Top 3 scores: {top_3}")
