# From: Zero to AI Agent, Chapter 4, Section 4.6
# when_to_use_sets.py - When to choose sets for your data

# 1. You need only unique items
unique_visitors = set()
unique_visitors.add("user123")
unique_visitors.add("user456")
unique_visitors.add("user123")  # Won't be added again
print(unique_visitors)  # {'user123', 'user456'}

# 2. You need FAST membership testing
valid_commands = {"start", "stop", "pause", "resume"}
user_input = "start"
if user_input in valid_commands:  # Super fast!
    print("Valid command")

# 3. You need set operations (union, intersection, difference)
skills_required = {"Python", "SQL", "ML"}
skills_candidate = {"Python", "SQL", "Java", "ML"}
has_all_required = skills_required.issubset(skills_candidate)  # True

# 4. Removing duplicates from data
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_numbers = list(set(numbers))  # [1, 2, 3, 4]

# 5. Finding commonalities or differences
team_a = {"Python", "JavaScript", "Go"}
team_b = {"Python", "Java", "C++"}
common_languages = team_a & team_b  # {'Python'}

# Real-world SET examples in AI:

# Tracking unique entities in conversations
mentioned_topics = set()
mentioned_topics.add("weather")
mentioned_topics.add("sports")
mentioned_topics.add("weather")  # Duplicate ignored

# Vocabulary in NLP
text = "the cat sat on the mat"
vocabulary = set(text.split())  # Unique words only

# Feature selection
all_features = {"f1", "f2", "f3", "f4", "f5"}
selected_features = {"f1", "f3", "f5"}
excluded_features = all_features - selected_features

print("Set examples:")
print(f"Unique visitors: {unique_visitors}")
print(f"Has all required skills: {has_all_required}")
print(f"Common languages: {common_languages}")
print(f"Vocabulary size: {len(vocabulary)}")
print(f"Excluded features: {excluded_features}")
