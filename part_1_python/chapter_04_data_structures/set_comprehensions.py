# From: Zero to AI Agent, Chapter 4, Section 4.5
# set_comprehensions.py - Creating sets elegantly

# Basic set comprehension
squares = {x**2 for x in range(10)}
print(f"Squares: {squares}")

# With condition
even_squares = {x**2 for x in range(10) if x % 2 == 0}
print(f"Even squares: {even_squares}")

# From string - unique words longer than 3 characters
text = "the quick brown fox jumps over the lazy fox"
long_words = {word for word in text.split() if len(word) > 3}
print(f"Long words: {long_words}")

# Normalizing data
emails = ["Alice@EXAMPLE.com", "bob@example.com", "ALICE@Example.com", "charlie@test.com"]
unique_emails = {email.lower() for email in emails}
print(f"Unique emails (normalized): {unique_emails}")

# Extracting from nested data
users = [
    {"name": "Alice", "tags": ["python", "ai", "ml"]},
    {"name": "Bob", "tags": ["python", "web", "api"]},
    {"name": "Charlie", "tags": ["ai", "data", "python"]}
]

all_tags = {tag for user in users for tag in user["tags"]}
print(f"All unique tags: {all_tags}")
