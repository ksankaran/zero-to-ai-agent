# From: Zero to AI Agent, Chapter 5, Section 5.7
# File: use_my_tools.py

# file: use_my_tools.py
import my_tools

# Use functions from your module!
greeting = my_tools.greet("Alice")
print(greeting)

age = my_tools.calculate_age(2000)
print(f"Someone born in 2000 is {age} years old")

if my_tools.is_even(42):
    print("42 is even!")

# Access module variables
print(f"Using my_tools version {my_tools.VERSION}")