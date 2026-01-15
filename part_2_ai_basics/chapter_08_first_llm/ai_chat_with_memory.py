# From: Zero to AI Agent, Chapter 8, Section 8.1
# File: ai_chat_with_memory.py

import openai
import os
from pathlib import Path

# Load API key (same as before)
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
    print("❌ No API key found! Run setup_api_key.py first!")
    exit()

client = openai.OpenAI(api_key=api_key)

print("🤖 AI Assistant with Memory!")
print("I'll remember our conversation now!")
print("Commands: 'quit' to exit, 'forget' to clear memory")
print("-" * 40)

# This list will store our conversation history!
conversation = [
    {"role": "system", "content": "You are a helpful, friendly assistant."}
]

while True:
    user_message = input("\nYou: ")
    
    if user_message.lower() == 'quit':
        print("👋 Bye! Thanks for chatting!")
        break
    
    if user_message.lower() == 'forget':
        # Clear the conversation history
        conversation = [conversation[0]]  # Keep only system message
        print("🧹 Memory cleared! Fresh start!")
        continue
    
    # Add user message to conversation history
    conversation.append({"role": "user", "content": user_message})
    
    # Send the ENTIRE conversation to the AI
    # This is how it remembers what you talked about!
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation  # <- The magic! Send all messages!
    )
    
    # Get and show the response
    ai_message = response.choices[0].message.content
    print(f"\nAI: {ai_message}")
    
    # Add AI's response to conversation history
    conversation.append({"role": "assistant", "content": ai_message})
    
    # Keep conversation from getting too long (optional)
    if len(conversation) > 20:
        # Keep system message and last 19 messages
        conversation = [conversation[0]] + conversation[-19:]

print("\n🎉 You just built a chatbot with memory!")
