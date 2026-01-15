# From: Zero to AI Agent, Chapter 6, Section 6.2
# File: json_intro.py

# This is a Python dictionary
python_data = {
    "name": "Alice",
    "age": 28,
    "is_student": False,
    "grades": [95, 87, 92],
    "address": {
        "street": "123 Python St",
        "city": "Codeville"
    }
}

# This is what it looks like in JSON (almost identical!)
json_string = '''
{
    "name": "Alice",
    "age": 28,
    "is_student": false,
    "grades": [95, 87, 92],
    "address": {
        "street": "123 Python St",
        "city": "Codeville"
    }
}
'''

print("See how similar they are? Just a few differences:")
print("1. JSON uses 'true/false' instead of 'True/False'")
print("2. JSON uses 'null' instead of 'None'")
print("3. JSON requires double quotes for strings")
print("\nThat's it! Python makes JSON feel natural! 🎯")
