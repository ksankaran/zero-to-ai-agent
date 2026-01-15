# converting_to_boolean.py
# From: Zero to AI Agent, Chapter 2, Section 2.5
# Understanding boolean conversion

print("=== Converting to Boolean ===")

# Numbers to boolean
print("Numbers:")
print(f"bool(0) = {bool(0)}")           # False
print(f"bool(1) = {bool(1)}")           # True
print(f"bool(-5) = {bool(-5)}")         # True
print(f"bool(0.0) = {bool(0.0)}")       # False
print(f"bool(0.1) = {bool(0.1)}")       # True

# Strings to boolean
print("\nStrings:")
print(f"bool('') = {bool('')}")         # False (empty)
print(f"bool('hello') = {bool('hello')}") # True
print(f"bool(' ') = {bool(' ')}")       # True (space is not empty!)
print(f"bool('False') = {bool('False')}") # True (non-empty string!)

# Common mistake with string booleans
print("\n=== Common Mistake ===")
user_input = "False"  # User typed the word "False"
wrong_way = bool(user_input)  # This is True! (non-empty string)
print(f"bool('{user_input}') = {wrong_way} (UNEXPECTED!)")

# Correct way to convert string "True"/"False"
right_way = user_input.lower() == "true"
print(f"'{user_input}'.lower() == 'true' = {right_way} (CORRECT!)")
