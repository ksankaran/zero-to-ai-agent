# From: Zero to AI Agent, Chapter 4, Section 4.4
# nested_dictionaries.py - Working with complex nested data structures

# Complex AI conversation data
conversation = {
    "id": "conv_123",
    "user": {
        "name": "Alice",
        "id": "user_456",
        "preferences": {
            "language": "en",
            "style": "concise"
        }
    },
    "messages": [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there!"},
        {"role": "user", "content": "What's the weather?"}
    ],
    "metadata": {
        "created": "2024-01-15",
        "model": "gpt-3.5-turbo",
        "token_count": 45
    }
}

# Accessing nested data
user_name = conversation["user"]["name"]
language = conversation["user"]["preferences"]["language"]
first_message = conversation["messages"][0]["content"]
token_count = conversation["metadata"]["token_count"]

print(f"User: {user_name} (language: {language})")
print(f"First message: {first_message}")
print(f"Tokens used: {token_count}")

# Safely navigating nested structures
# Use get() chains for safety
style = conversation.get("user", {}).get("preferences", {}).get("style", "default")
print(f"Style preference: {style}")

# Modifying nested data
conversation["metadata"]["token_count"] += 10
conversation["user"]["preferences"]["style"] = "detailed"
print(f"\nUpdated token count: {conversation['metadata']['token_count']}")
print(f"Updated style: {conversation['user']['preferences']['style']}")
