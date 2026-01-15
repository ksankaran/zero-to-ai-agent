# From: Zero to AI Agent, Chapter 5, Section 5.6
# File: json_module_demo.py

import json

# Python dictionary to JSON string
person = {
    "name": "Alice",
    "age": 30,
    "skills": ["Python", "AI", "Machine Learning"],
    "is_student": True
}

# Convert to JSON string
json_string = json.dumps(person, indent=2)
print("JSON string:")
print(json_string)

# Save to a file
with open("person.json", "w") as f:
    json.dump(person, f, indent=2)
print("Saved to person.json!")

# Load from JSON string
loaded_person = json.loads(json_string)
print(f"Loaded name: {loaded_person['name']}")

# Load from file
with open("person.json", "r") as f:
    file_person = json.load(f)
print(f"Loaded from file: {file_person}")