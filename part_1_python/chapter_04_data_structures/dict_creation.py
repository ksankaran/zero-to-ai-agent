# From: Zero to AI Agent, Chapter 4, Section 4.4
# dict_creation.py - Creating dictionaries in Python

# Your first dictionary - a user profile
user = {
    "name": "Alice",
    "age": 28,
    "email": "alice@example.com",
    "is_premium": True
}

print("User dictionary:", user)
print(f"Type: {type(user)}")

# Keys can be strings, numbers, or any immutable type (remember tuples?)
mixed_keys = {
    "string_key": "I'm a string value",
    42: "I'm accessed with the number 42",
    (1, 2): "I'm accessed with the tuple (1, 2)",
    3.14: "I'm accessed with 3.14"
}

print("\nMixed keys dictionary:")
for key, value in mixed_keys.items():
    print(f"  {key} -> {value}")

# Empty dictionary (ready to fill!)
empty_dict = {}
also_empty = dict()  # Alternative way
print(f"\nEmpty dict: {empty_dict}")
print(f"Also empty: {also_empty}")

# Creating from pairs
pairs = [("red", "#FF0000"), ("green", "#00FF00"), ("blue", "#0000FF")]
color_codes = dict(pairs)
print(f"\nColor codes from pairs: {color_codes}")

# Using dict() with keyword arguments
person = dict(name="Bob", age=30, city="New York")
print(f"\nPerson created with dict(): {person}")
