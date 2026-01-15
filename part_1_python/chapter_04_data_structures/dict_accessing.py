# From: Zero to AI Agent, Chapter 4, Section 4.4
# dict_accessing.py - Accessing dictionary values safely

# AI model configuration
model_config = {
    "model_name": "GPT-3",
    "temperature": 0.7,
    "max_tokens": 2048,
    "top_p": 0.95,
    "frequency_penalty": 0.5,
    "presence_penalty": 0.0
}

# Access values using keys
model = model_config["model_name"]
temp = model_config["temperature"]
print(f"Model: {model} with temperature: {temp}")

# Safer access with get() method
tokens = model_config.get("max_tokens")
print(f"Max tokens: {tokens}")

# get() with default value if key doesn't exist
stream = model_config.get("stream", False)  # Default to False if not found
print(f"Stream enabled: {stream}")

# What happens when key doesn't exist?
# bad_access = model_config["non_existent"]  # KeyError!

# Safe pattern for checking if key exists
if "top_p" in model_config:
    print(f"Top-p sampling: {model_config['top_p']}")

# Check if key doesn't exist
if "api_key" not in model_config:
    print("No API key in config (good for security!)")
