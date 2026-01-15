# From: Zero to AI Agent, Chapter 6, Section 6.2
# File: json_pitfalls.py

import json
import math
import os

print("🚨 COMMON JSON PROBLEMS & SOLUTIONS\n")

# Problem 1: Single quotes don't work in JSON
print("="*50)
print("Problem 1: Single quotes in JSON strings")

bad_json = "{'name': 'Alice'}"  # This is NOT valid JSON!
print(f"Bad JSON: {bad_json}")

try:
    json.loads(bad_json)
except json.JSONDecodeError as e:
    print(f"❌ Error: {e}")

# Solution: Use double quotes
good_json = '{"name": "Alice"}'
print(f"✅ Good JSON: {good_json}")
data = json.loads(good_json)
print(f"✅ Parsed successfully: {data}")

# Problem 2: Trailing commas
print("\n" + "="*50)
print("Problem 2: Trailing commas")

bad_json_comma = '''
{
    "name": "Bob",
    "age": 25,  
}'''  # That trailing comma after 25 is invalid!

try:
    json.loads(bad_json_comma)
except json.JSONDecodeError as e:
    print(f"❌ Error: Trailing comma not allowed")

# Solution: Remove trailing commas
good_json_comma = '''
{
    "name": "Bob",
    "age": 25
}'''
print("✅ Removed trailing comma - works now!")

# Problem 3: Comments aren't allowed in JSON
print("\n" + "="*50)
print("Problem 3: JSON doesn't support comments")

json_with_comments = '''
{
    // This is a comment - but JSON doesn't allow it!
    "name": "Charlie"
}'''

try:
    json.loads(json_with_comments)
except json.JSONDecodeError:
    print("❌ Comments cause JSON parsing to fail")

# Solution: Remove comments before parsing or use a different format
print("✅ Solution: Remove comments or use configuration files that support them")

# Problem 4: NaN and Infinity
print("\n" + "="*50)
print("Problem 4: Special float values")

problematic = {
    "normal": 3.14,
    "not_a_number": float('nan'),
    "infinity": float('inf')
}

# This can cause issues!
try:
    # Standard JSON doesn't support NaN/Infinity
    result = json.dumps(problematic)
    print(f"⚠️  Python allows it but creates non-standard JSON: {result}")
except ValueError as e:
    print(f"Some JSON libraries reject NaN/Infinity: {e}")

# Solution: Handle special values explicitly
def clean_floats(obj):
    if isinstance(obj, float):
        if math.isnan(obj):
            return None  # or "NaN" as string
        elif math.isinf(obj):
            return None  # or "Infinity" as string
    return obj

cleaned = {k: clean_floats(v) for k, v in problematic.items()}
print(f"✅ Cleaned data: {json.dumps(cleaned)}")

# Problem 5: Circular references
print("\n" + "="*50)
print("Problem 5: Circular references")

# This creates a circular reference
data = {"name": "loop"}
data["self"] = data  # Points to itself!

try:
    json.dumps(data)
except ValueError as e:
    print(f"❌ Circular reference error: {e}")

# Solution: Break circular references
data_safe = {"name": "loop", "self": None}  # or reference by ID
print(f"✅ Safe version: {json.dumps(data_safe)}")

# Problem 6: Large numbers precision
print("\n" + "="*50)
print("Problem 6: Large number precision")

large_number = 12345678901234567890
json_str = json.dumps({"big": large_number})
parsed = json.loads(json_str)

print(f"Original: {large_number}")
print(f"After JSON round-trip: {parsed['big']}")
print(f"✅ Python handles large integers well!")

# Problem 7: Reading malformed JSON files
print("\n" + "="*50)
print("Problem 7: Handling malformed JSON files")

# Create a file with slightly broken JSON
with open("broken.json", "w") as f:
    f.write('{"name": "Test" "age": 25}')  # Missing comma!

try:
    with open("broken.json", "r") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"❌ JSON parsing error: {e}")
    print(f"   Line {e.lineno}, Column {e.colno}")
    print("✅ Solution: Check the file at the indicated position")

# Clean up
os.remove("broken.json")
