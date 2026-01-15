# From: Zero to AI Agent, Chapter 8, Section 8.1
# File: my_first_ai_chat.py

import openai
import os
from pathlib import Path

# Load your API key from .env file
def load_api_key():
    """Load API key from .env file"""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

# Get your API key
api_key = load_api_key()
if not api_key:
    print("❌ No API key found! Run setup_api_key.py first!")
    exit()

# THIS IS IT - YOUR FIRST AI CALL! 🚀
client = openai.OpenAI(api_key=api_key)

print("🤖 AI Assistant Ready!")
print("Type 'quit' to exit")
print("-" * 40)

# Conversation loop
while True:
    # Get your message
    user_message = input("\nYou: ")
    
    if user_message.lower() == 'quit':
        print("👋 Bye! You just built your first AI app!")
        break
    
    # ✨ THE MAGIC HAPPENS HERE - WE CALL THE AI! ✨
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    
    # Get the AI's response
    ai_message = response.choices[0].message.content
    
    # Show the response
    print(f"\nAI: {ai_message}")

print("\n🎉 Congratulations! You just had your first AI conversation!")
