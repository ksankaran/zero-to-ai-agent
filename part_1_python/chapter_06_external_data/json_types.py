# From: Zero to AI Agent, Chapter 6, Section 6.2
# File: json_types.py

import json
from datetime import datetime

print("🎯 JSON SUPPORTS THESE TYPES:\n")

# What JSON can handle
json_friendly = {
    "strings": "Hello, World!",
    "numbers": 42,
    "floats": 3.14159,
    "booleans": True,  # Becomes 'true' in JSON
    "null_value": None,  # Becomes 'null' in JSON
    "lists": [1, 2, 3, "mixed", True],
    "objects": {
        "nested": "dictionaries",
        "are": "perfect"
    }
}

print("✅ This works perfectly:")
print(json.dumps(json_friendly, indent=2))

print("\n" + "="*50)
print("❌ JSON CANNOT HANDLE THESE DIRECTLY:\n")

# What JSON cannot handle
problematic_data = {
    "date": datetime.now(),
    "set": {1, 2, 3},
    "tuple": (1, 2, 3),
    "bytes": b"binary data",
    "function": print
}

# This would crash!
try:
    json.dumps(problematic_data)
except TypeError as e:
    print(f"Error: {e}")

print("\n" + "="*50)
print("✅ BUT WE CAN WORK AROUND IT:\n")

# Solutions for unsupported types
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert to string
        return super().default(obj)

# Manual conversion approach
converted_data = {
    "date": datetime.now().isoformat(),  # Convert to string
    "set": list({1, 2, 3}),  # Convert to list
    "tuple": list((1, 2, 3)),  # Convert to list
    "bytes": "binary data",  # Convert to string
    # Skip the function - can't serialize that!
}

print("Converted data:")
print(json.dumps(converted_data, indent=2))

# Using custom encoder for dates
data_with_date = {
    "created": datetime.now(),
    "user": "Alice",
    "action": "login"
}

json_with_date = json.dumps(data_with_date, cls=DateTimeEncoder, indent=2)
print("\nWith custom encoder:")
print(json_with_date)
