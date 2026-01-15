# From: Zero to AI Agent, Chapter 4, Section 4.1
# Exercise 2: Grade Analyzer

# 1. Create list of test scores
scores = [85, 92, 78, 95, 88, 73, 91, 82, 79, 96]
print("Test scores:", scores)

# 2. Find highest score
highest = max(scores)
print(f"Highest score: {highest}")

# 3. Find lowest score
lowest = min(scores)
print(f"Lowest score: {lowest}")

# 4. Calculate average
average = sum(scores) / len(scores)
print(f"Average score: {average:.2f}")

# 5. Extract top 3 scores using slicing after sorting
sorted_scores = sorted(scores, reverse=True)
top_3 = sorted_scores[:3]
print(f"Top 3 scores: {top_3}")

# 6. Count scores above 85
above_85 = 0
for score in scores:
    if score > 85:
        above_85 += 1
print(f"Scores above 85: {above_85}")
