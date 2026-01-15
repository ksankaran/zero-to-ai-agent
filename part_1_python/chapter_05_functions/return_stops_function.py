# From: Zero to AI Agent, Chapter 5, Section 5.3
# File: return_stops_function.py

def check_age(age):
    if age < 0:
        return "Error: Age can't be negative!"  # Function stops here if true
    
    if age < 18:
        return "You're a minor"  # Function stops here if true
    
    if age < 65:
        return "You're an adult"  # Function stops here if true
    
    return "You're a senior"  # Only reaches here if age >= 65

# Test it
print(check_age(-5))   # Error: Age can't be negative!
print(check_age(10))   # You're a minor
print(check_age(30))   # You're an adult
print(check_age(70))   # You're a senior