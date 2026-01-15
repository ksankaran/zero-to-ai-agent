# From: Zero to AI Agent, Chapter 4, Section 4.4
# json_and_apis.py - Working with JSON and API responses

# Simulating an API response (this is what you'll get from OpenAI, etc.)
api_response = {
    "id": "chatcmpl-123",
    "object": "chat.completion",
    "created": 1677652288,
    "model": "gpt-3.5-turbo",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "The weather today is sunny with a high of 72°F."
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 12,
        "completion_tokens": 15,
        "total_tokens": 27
    }
}

# Extracting the actual response
assistant_message = api_response["choices"][0]["message"]["content"]
total_tokens = api_response["usage"]["total_tokens"]
model_used = api_response["model"]

print(f"Model: {model_used}")
print(f"Response: {assistant_message}")
print(f"Tokens used: {total_tokens}")

# Converting to/from JSON (you'll use this constantly!)
import json

# Dictionary to JSON string
json_string = json.dumps({"name": "Alice", "age": 30}, indent=2)
print(f"\nJSON string:\n{json_string}")

# JSON string back to dictionary
parsed = json.loads(json_string)
print(f"\nParsed back to dict: {parsed}")
