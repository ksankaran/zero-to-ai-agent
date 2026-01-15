# From: Zero to AI Agent, Chapter 4, Section 4.5
# set_mathematics.py - Mathematical set operations

# Two teams and their programming languages
team_a = {"Python", "JavaScript", "Go", "Rust"}
team_b = {"Python", "Java", "JavaScript", "C++"}

print(f"Team A knows: {team_a}")
print(f"Team B knows: {team_b}")

# UNION - All languages known by either team (OR)
all_languages = team_a | team_b  # Using | operator
# OR
all_languages = team_a.union(team_b)  # Using method
print(f"\nAll languages (union): {all_languages}")

# INTERSECTION - Languages known by both teams (AND)
common_languages = team_a & team_b  # Using & operator
# OR
common_languages = team_a.intersection(team_b)  # Using method
print(f"Common languages (intersection): {common_languages}")

# DIFFERENCE - Languages only Team A knows
team_a_exclusive = team_a - team_b  # Using - operator
# OR
team_a_exclusive = team_a.difference(team_b)  # Using method
print(f"Only Team A knows (difference): {team_a_exclusive}")

# SYMMETRIC DIFFERENCE - Languages known by one team but not both (XOR)
unique_to_one_team = team_a ^ team_b  # Using ^ operator
# OR
unique_to_one_team = team_a.symmetric_difference(team_b)  # Using method
print(f"Known by only one team (symmetric difference): {unique_to_one_team}")

# Real-world example: Finding common interests
alice_interests = {"AI", "Python", "Reading", "Hiking", "Photography"}
bob_interests = {"Python", "Gaming", "AI", "Cooking", "Photography"}

common = alice_interests & bob_interests
print(f"\nAlice and Bob both like: {common}")

alice_unique = alice_interests - bob_interests
print(f"Only Alice likes: {alice_unique}")

all_interests = alice_interests | bob_interests
print(f"All interests combined: {all_interests}")
