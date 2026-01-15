# From: Zero to AI Agent, Chapter 6, Section 6.2
# File: json_formatting.py

import json

# Compact vs Pretty JSON
data = {
    "name": "Alice",
    "scores": [95, 87, 92, 88],
    "details": {
        "age": 25,
        "city": "NYC"
    }
}

print("COMPACT JSON (minified - good for transmission):")
compact = json.dumps(data, separators=(',', ':'))  # No spaces
print(compact)
print(f"Size: {len(compact)} characters")

print("\n" + "="*50)
print("PRETTY JSON (readable - good for humans):")
pretty = json.dumps(data, indent=4)
print(pretty)
print(f"Size: {len(pretty)} characters")

print("\n" + "="*50)
print("SORTED KEYS (consistent ordering):")
sorted_json = json.dumps(data, indent=4, sort_keys=True)
print(sorted_json)

# Custom formatting
print("\n" + "="*50)
print("CUSTOM FORMATTING:")

def format_json_for_display(data):
    """Format JSON with custom settings"""
    return json.dumps(
        data,
        indent=2,  # 2 spaces instead of 4
        sort_keys=True,  # Alphabetical order
        ensure_ascii=False  # Allow Unicode characters
    )

unicode_data = {
    "greeting": "Hello! 👋",
    "languages": ["Python 🐍", "JavaScript ⚡", "Rust 🦀"],
    "status": "Learning JSON 📚"
}

formatted = format_json_for_display(unicode_data)
print(formatted)

# One-liner for debugging
print("\n" + "="*50)
print("QUICK DEBUGGING FORMAT:")

# Create a one-line function for pretty printing during debugging
def pp(data):
    """Pretty print helper for debugging"""
    print(json.dumps(data, indent=2, default=str))

complex_data = {
    "user": {"name": "Bob", "id": 123},
    "actions": ["login", "view", "logout"],
    "timestamp": "2024-01-15"
}

print("Using pp() helper:")
pp(complex_data)
