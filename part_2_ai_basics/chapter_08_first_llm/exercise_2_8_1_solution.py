# From: Zero to AI Agent, Chapter 8, Section 8.1
# File: exercise_2_8_1_conversation_saver.py

import openai
import json
from pathlib import Path
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

def save_conversation(messages, message_count):
    """Save conversation to a file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversation_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        f.write(f"Conversation saved at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total messages exchanged: {message_count}\n")
        f.write("=" * 50 + "\n\n")
        
        for msg in messages:
            if msg["role"] != "system":
                role = "You" if msg["role"] == "user" else "AI"
                f.write(f"{role}: {msg['content']}\n\n")
    
    return filename

def load_conversation(filename):
    """Load a previous conversation from JSON file"""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data["messages"], data["message_count"]
    except:
        print("Could not load conversation file")
        return None, 0

# Setup
api_key = load_api_key()
if not api_key:
    print("❌ No API key found! Run setup_api_key.py first!")
    exit()

client = openai.OpenAI(api_key=api_key)

print("💾 Conversation Saver Bot!")
print("Commands: 'quit', 'save', 'load', 'count'")
print("-" * 40)

# Check if user wants to load previous conversation
load_previous = input("Load previous conversation? (y/n): ").lower() == 'y'

conversation = [{"role": "system", "content": "You are a helpful assistant."}]
message_count = 0

if load_previous:
    # List available conversation files
    conv_files = list(Path(".").glob("conversation_*.json"))
    if conv_files:
        print("\nAvailable conversations:")
        for i, f in enumerate(conv_files, 1):
            print(f"  {i}. {f.name}")
        
        choice = input("Choose file (number): ")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(conv_files):
                loaded_conv, loaded_count = load_conversation(conv_files[idx])
                if loaded_conv:
                    conversation = loaded_conv
                    message_count = loaded_count
                    print(f"✅ Loaded conversation with {message_count} messages")
                    
                    # Show last message if exists
                    for msg in reversed(conversation):
                        if msg["role"] == "assistant":
                            print(f"\nLast AI message: {msg['content'][:100]}...")
                            break
        except:
            print("Could not load file, starting fresh")

while True:
    user_message = input("\nYou: ")
    
    if user_message.lower() == 'quit':
        # Auto-save on quit
        if message_count > 0:
            filename = save_conversation(conversation, message_count)
            print(f"💾 Conversation saved to {filename}")
        print("👋 Goodbye!")
        break
    
    if user_message.lower() == 'save':
        filename = save_conversation(conversation, message_count)
        print(f"💾 Conversation saved to {filename}")
        
        # Also save as JSON for loading later
        json_filename = filename.replace('.txt', '.json')
        with open(json_filename, 'w') as f:
            json.dump({
                "messages": conversation,
                "message_count": message_count,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        print(f"📄 Also saved as {json_filename} for loading later")
        continue
    
    if user_message.lower() == 'count':
        print(f"📊 Messages exchanged: {message_count}")
        user_messages = sum(1 for m in conversation if m["role"] == "user")
        ai_messages = sum(1 for m in conversation if m["role"] == "assistant")
        print(f"   Your messages: {user_messages}")
        print(f"   AI messages: {ai_messages}")
        continue
    
    # Add user message
    conversation.append({"role": "user", "content": user_message})
    message_count += 1
    
    # Get AI response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    
    ai_message = response.choices[0].message.content
    print(f"\nAI: {ai_message}")
    
    # Add to conversation
    conversation.append({"role": "assistant", "content": ai_message})
    message_count += 1
    
    # Show message count every 5 messages
    if message_count % 5 == 0:
        print(f"\n[{message_count} messages exchanged]")

print(f"\n📊 Final message count: {message_count}")
