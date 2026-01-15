# From: Zero to AI Agent, Chapter 4, Section 4.4
# dict_methods.py - Essential dictionary methods

# Sample data: User preferences for an AI assistant
preferences = {
    "language": "en",
    "voice": "neutral",
    "speed": "normal",
    "personality": "helpful",
    "memory": True
}

# keys() - Get all keys
all_keys = preferences.keys()
print("All preference keys:", list(all_keys))

# values() - Get all values
all_values = preferences.values()
print("All preference values:", list(all_values))

# items() - Get key-value pairs
print("\nAll preferences:")
for key, value in preferences.items():
    print(f"  {key}: {value}")

# pop() with default
removed = preferences.pop("non_existent", "default_value")
print(f"\nPopped non-existent key: {removed}")

# setdefault() - Get value or set it if missing
theme = preferences.setdefault("theme", "dark")
print(f"Theme (set to default): {theme}")
print(f"Preferences now include theme: {preferences}")

# Copy dictionary (remember the list copying lesson?)
backup = preferences.copy()
backup["language"] = "es"
print(f"\nOriginal language: {preferences['language']}")
print(f"Backup language: {backup['language']}")
