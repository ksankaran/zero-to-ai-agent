# comparison_operators.py
# From: Zero to AI Agent, Chapter 2, Section 2.4
# All the ways to compare values in Python

# Equality and inequality
password = "secret123"
user_input = "secret123"
print("=== Equality Checks ===")
print(f"password == user_input: {password == user_input}")  # True
print(f"5 == 5: {5 == 5}")                                  # True
print(f"5 != 3: {5 != 3}")                                  # True (not equal)
print(f"'hello' == 'Hello': {'hello' == 'Hello'}")         # False (case matters!)

# Greater than and less than
print("\n=== Comparison Checks ===")
temperature = 75
print(f"temperature = {temperature}")
print(f"temperature > 70: {temperature > 70}")      # True
print(f"temperature < 80: {temperature < 80}")      # True
print(f"temperature >= 75: {temperature >= 75}")    # True (equal counts!)
print(f"temperature <= 75: {temperature <= 75}")    # True

# Comparing strings (alphabetical order)
print("\n=== String Comparisons ===")
print(f"'apple' < 'banana': {'apple' < 'banana'}")  # True (a comes before b)
print(f"'Zoo' < 'ant': {'Zoo' < 'ant'}")           # True (Capital Z < lowercase a!)

# Membership testing with 'in'
print("\n=== Membership Tests ===")
fruits = ["apple", "banana", "orange"]
print(f"'banana' in fruits: {'banana' in fruits}")          # True
print(f"'grape' in fruits: {'grape' in fruits}")           # False
print(f"'a' in 'team': {'a' in 'team'}")                   # True
print(f"'I' not in 'team': {'I' not in 'team'}")          # True (there's no I in team!)
