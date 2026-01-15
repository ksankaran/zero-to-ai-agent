# From: Zero to AI Agent, Chapter 5, Section 5.7
# File: my_tools.py

# file: my_tools.py
"""
My personal collection of useful functions.
Created while learning Python and AI development!
"""

def greet(name):
    """Generate a friendly greeting"""
    return f"Hello, {name}! Welcome to Python programming!"

def calculate_age(birth_year, current_year=2024):
    """Calculate age from birth year"""
    return current_year - birth_year

def is_even(number):
    """Check if a number is even"""
    return number % 2 == 0

# Module-level variable
VERSION = "1.0.0"
AUTHOR = "Your Name"

# This runs only when the module is run directly, not when imported
if __name__ == "__main__":
    print(f"My Tools Module v{VERSION} by {AUTHOR}")
    print("This module contains helpful functions!")
    print("Import it in another file to use the functions.")