# From: Zero to AI Agent, Chapter 5, Section 5.4
# File: variable_shadowing.py

name = "Global Alice"  # Global variable

def greet():
    name = "Local Bob"  # Local variable with same name
    print(f"Hello, {name}")  # Uses local version

greet()  # Prints: Hello, Local Bob
print(f"Outside: {name}")  # Prints: Outside: Global Alice