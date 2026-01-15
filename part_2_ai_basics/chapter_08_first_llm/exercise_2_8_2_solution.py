# From: Zero to AI Agent, Chapter 8, Section 8.2
# File: exercise_2_8_2_conversation_counter.py

import openai
from pathlib import Path
import json
from datetime import datetime

def load_api_key():
    """Load API key from .env file"""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

api_key = load_api_key()
if not api_key:
    print("❌ No API key found!")
    exit()

client = openai.OpenAI(api_key=api_key)

print("💬 Conversation Counter Bot")
print("=" * 50)
print("I'll count messages and track costs!")
print("Type 'quit' to exit and save")
print("-" * 50)

# Tracking variables
message_count = 0
total_words = 0
estimated_cost = 0.0
conversation = []

while True:
    user_input = input(f"\n[Message #{message_count + 1}] You: ")
    
    if user_input.lower() == 'quit':
        break
    
    # Count this message
    message_count += 1
    user_words = len(user_input.split())
    
    # Add to conversation
    conversation.append({"role": "user", "content": user_input})
    
    # Make API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    
    ai_response = response.choices[0].message.content
    ai_words = len(ai_response.split())
    total_words += user_words + ai_words
    
    # Estimate cost (roughly 750 words = 1000 tokens = $0.002)
    tokens_used = response.usage.total_tokens if response.usage else (total_words * 1.3)
    call_cost = (tokens_used / 1000) * 0.002
    estimated_cost += call_cost
    
    print(f"\nAI: {ai_response}")
    print(f"\n📊 Stats: {ai_words} words | Cost: ${call_cost:.6f} | Total: ${estimated_cost:.6f}")
    
    # Add AI response to conversation
    conversation.append({"role": "assistant", "content": ai_response})

# Save conversation
if conversation:
    filename = f"counted_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w') as f:
        json.dump({
            "conversation": conversation,
            "stats": {
                "messages": message_count,
                "total_words": total_words,
                "estimated_cost": estimated_cost
            },
            "timestamp": datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"\n💾 Saved to {filename}")

# Final stats
print("\n" + "=" * 50)
print("📊 Final Statistics:")
print(f"  Messages sent: {message_count}")
print(f"  Total words: {total_words}")
print(f"  Estimated cost: ${estimated_cost:.6f}")
if message_count > 0:
    print(f"  Average cost per message: ${estimated_cost/message_count:.6f}")

print("\n👋 Thanks for chatting!")
