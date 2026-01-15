# From: Zero to AI Agent, Chapter 8, Section 8.2
# File: smart_conversation.py

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

print("💬 Smart Conversation Manager")
print("Keeps only recent messages to save tokens!")
print("Commands: 'quit', 'count'")
print("-" * 40)

# Our conversation history
conversation = [
    {"role": "system", "content": "You are a helpful assistant."}
]

MAX_MESSAGES = 10  # Keep only last 10 messages

while True:
    user_input = input("\nYou: ")
    
    if user_input.lower() == 'quit':
        break
    
    if user_input.lower() == 'count':
        print(f"📊 Messages in memory: {len(conversation) - 1}")  # -1 for system message
        continue
    
    # Add user message
    conversation.append({"role": "user", "content": user_input})
    
    # Keep conversation from getting too long
    if len(conversation) > MAX_MESSAGES:
        # Keep system message (first) and recent messages
        conversation = [conversation[0]] + conversation[-(MAX_MESSAGES-1):]
        print("(Trimmed old messages to save tokens)")
    
    # Make API call with conversation history
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    
    ai_message = response.choices[0].message.content
    print(f"\nAI: {ai_message}")
    
    # Add AI response to history
    conversation.append({"role": "assistant", "content": ai_message})

print("\n✅ Smart conversation management - you're saving money already!")
