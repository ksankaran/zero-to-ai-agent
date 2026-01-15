# From: Zero to AI Agent, Chapter 5, Section 5.4
# File: scope_mystery.py

def create_message():
    secret = "Functions are awesome!"
    print(f"Inside function: {secret}")

create_message()
print(f"Outside function: {secret}")  # This will cause an error!