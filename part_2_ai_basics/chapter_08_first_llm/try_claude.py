# From: Zero to AI Agent, Chapter 8, Section 8.1
# File: try_claude.py (if you have an Anthropic API key)

import anthropic
from pathlib import Path

# Load API key from .env
def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('ANTHROPIC_API_KEY='):
                    return line.split('=')[1].strip()
    return None

api_key = load_api_key()
if not api_key:
    print("No Anthropic API key found. Add ANTHROPIC_API_KEY to your .env file!")
    exit()

# Create Claude client
client = anthropic.Anthropic(api_key=api_key)

# Ask Claude something!
message = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Tell me a short joke!"}
    ]
)

print("🤖 Claude says:")
print(message.content[0].text)
