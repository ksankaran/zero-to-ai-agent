# From: Zero to AI Agent, Chapter 5, Section 5.4
# File: global_scope_demo.py

# Global variable - created outside any function
favorite_language = "Python"

def print_favorite():
    # Functions CAN see global variables
    print(f"My favorite language is {favorite_language}")

def print_another():
    # Other functions can see it too
    print(f"Still loving {favorite_language}!")

print_favorite()      # My favorite language is Python
print_another()       # Still loving Python!
print(favorite_language)  # Python (works here too!)