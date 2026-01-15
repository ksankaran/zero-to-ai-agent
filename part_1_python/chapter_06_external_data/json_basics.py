# From: Zero to AI Agent, Chapter 6, Section 6.2
# File: json_basics.py

import json

# Creating some Python data
user_profile = {
    "username": "pythonista",
    "level": 5,
    "experience": 1250,
    "inventory": ["sword", "shield", "health_potion"],
    "stats": {
        "health": 100,
        "mana": 50,
        "strength": 15
    },
    "is_premium": True,
    "last_login": None  # This becomes 'null' in JSON
}

print("Original Python data:")
print(user_profile)
print(f"Type: {type(user_profile)}")

# Convert Python to JSON string (serialization)
json_string = json.dumps(user_profile, indent=4)  # indent makes it pretty!
print("\n" + "="*50)
print("As JSON string:")
print(json_string)
print(f"Type: {type(json_string)}")  # It's just a string!

# Convert JSON string back to Python (deserialization)
restored_data = json.loads(json_string)
print("\n" + "="*50)
print("Back to Python:")
print(restored_data)
print(f"Type: {type(restored_data)}")

# Verify it's the same
print("\n" + "="*50)
print(f"Are they equal? {user_profile == restored_data}")
print("Perfect round trip! 🎉")
