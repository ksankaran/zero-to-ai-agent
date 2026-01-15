# From: Zero to AI Agent, Chapter 5, Section 5.5
# File: lambda_transforming_pattern.py

# 3. TRANSFORMING - Change each item
names = ["alice", "bob", "charlie"]

# Capitalize each name
capitalized = list(map(lambda name: name.capitalize(), names))
print(f"Capitalized: {capitalized}")  # ['Alice', 'Bob', 'Charlie']

# Create email addresses
emails = list(map(lambda name: f"{name}@example.com", names))
print(f"Emails: {emails}")