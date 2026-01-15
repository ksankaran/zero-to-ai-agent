# From: Zero to AI Agent, Chapter 8, Section 8.2
# File: streaming_demo.py

import openai
from pathlib import Path

def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

api_key = load_api_key()
client = openai.OpenAI(api_key=api_key)

print("🌊 Streaming Chat Demo")
print("Watch the AI type its response!")
print("Type 'quit' to exit")
print("-" * 40)

while True:
    user_input = input("\nYou: ")
    
    if user_input.lower() == 'quit':
        break
    
    print("\nAI: ", end="", flush=True)
    
    # The magic parameter: stream=True
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_input}
        ],
        stream=True  # ← This makes it stream!
    )
    
    # Print each piece as it arrives
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    
    print()  # New line after response is complete

print("\n✨ That's how ChatGPT does it!")
