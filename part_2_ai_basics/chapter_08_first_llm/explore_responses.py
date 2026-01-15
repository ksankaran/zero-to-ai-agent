# From: Zero to AI Agent, Chapter 8, Section 8.3
# File: explore_responses.py

import openai
from pathlib import Path
from response_inspector import inspect_response, calculate_simple_cost

def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

# Setup
api_key = load_api_key()
if not api_key:
    print("❌ No API key found!")
    exit()

client = openai.OpenAI(api_key=api_key)

# Try a simple request
print("📤 Sending request: 'Say hello in 5 words'")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Say hello in 5 words"}],
    temperature=0.7
)

# Inspect what came back
inspect_response(response)

# Calculate cost
if response.usage:
    cost = calculate_simple_cost(response.usage.total_tokens)
    print(f"\n💰 Estimated cost: ${cost:.6f}")

# What's in the response object?
print("\n📦 Response object attributes:")
for attr in dir(response):
    if not attr.startswith('_'):
        print(f"  • {attr}")
