# From: Zero to AI Agent, Chapter 4, Section 4.2
# list_finding_counting.py - Finding and counting items in lists

# Sample data: user feedback scores
scores = [8, 9, 7, 9, 10, 8, 9, 7, 8, 9, 10, 9]
print("Feedback scores:", scores)

# count() - How many times does a value appear?
nines = scores.count(9)
tens = scores.count(10)
print(f"Number of 9s: {nines}")
print(f"Number of 10s: {tens}")

# index() - Where is a value located?
first_ten_position = scores.index(10)
print(f"First 10 is at position: {first_ten_position}")

# Be careful - index() raises an error if item doesn't exist!
# Safe way to use index():
search_value = 6
if search_value in scores:
    position = scores.index(search_value)
    print(f"Found {search_value} at position {position}")
else:
    print(f"{search_value} not found in scores")

# in operator - Check if item exists (returns True/False)
has_perfect_score = 10 in scores
has_failing_score = 5 in scores
print(f"Has perfect score (10)? {has_perfect_score}")
print(f"Has failing score (5)? {has_failing_score}")

# Real-world AI example: Checking for keywords in user input
user_message = "I want to cancel my subscription"
keywords = user_message.lower().split()
if "cancel" in keywords or "unsubscribe" in keywords:
    print("User wants to cancel - routing to retention team")
