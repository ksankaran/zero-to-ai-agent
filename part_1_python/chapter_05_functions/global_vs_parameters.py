# From: Zero to AI Agent, Chapter 5, Section 5.4
# File: global_vs_parameters.py

# BAD: Using global variables
score = 0  # Global

def add_points_bad():
    global score
    score += 10

def remove_points_bad():
    global score
    score -= 5

# GOOD: Using parameters and returns
def add_points_good(current_score, points):
    return current_score + points

def remove_points_good(current_score, points):
    return current_score - points

# Bad way - harder to track what's changing score
score = 0
add_points_bad()
remove_points_bad()
print(f"Final score: {score}")

# Good way - clear what goes in and comes out
score = 0
score = add_points_good(score, 10)
score = remove_points_good(score, 5)
print(f"Final score: {score}")