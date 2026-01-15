# From: Zero to AI Agent, Chapter 8, Section 8.1
# File: ai_chat_streaming.py

import openai
from pathlib import Path

# Load API key
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

print("🤖 Streaming AI Chat!")
print("Watch the AI 'type' its response!")
print("-" * 40)

while True:
    user_message = input("\nYou: ")
    
    if user_message.lower() == 'quit':
        break
    
    print("\nAI: ", end="", flush=True)
    
    # Add stream=True to see the response as it's generated!
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}],
        stream=True  # ← This makes it stream!
    )
    
    # Print each chunk as it arrives
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    
    print()  # New line after response

print("\n✨ Pretty cool, right?")
