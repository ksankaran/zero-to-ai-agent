# From: Zero to AI Agent, Chapter 8, Section 8.2
# File: exercise_3_8_2_personality_switcher.py

import openai
from pathlib import Path

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

# Define 3 personalities
personalities = {
    "teacher": {
        "name": "Professor Know",
        "system_message": "You are a patient teacher. Explain things clearly with examples. Be encouraging!",
        "temperature": 0.3,
        "emoji": "👨‍🏫"
    },
    "friend": {
        "name": "Buddy",
        "system_message": "You are a casual friend. Use simple language, be supportive, and add some humor!",
        "temperature": 0.9,
        "emoji": "😊"
    },
    "coach": {
        "name": "Coach Strong",
        "system_message": "You are a motivational coach. Be energetic, positive, and push people to be their best!",
        "temperature": 1.2,
        "emoji": "💪"
    }
}

# Start with teacher
current = "teacher"

print("🎭 Personality Switcher Bot")
print("=" * 50)
print("Commands: 'switch', 'who', 'quit'")
print(f"Starting with: {personalities[current]['emoji']} {personalities[current]['name']}")
print("-" * 50)

# Conversation history
conversation = [
    {"role": "system", "content": personalities[current]["system_message"]}
]

while True:
    personality = personalities[current]
    user_input = input(f"\n[{personality['emoji']}] You: ")
    
    if user_input.lower() == 'quit':
        print("👋 Goodbye!")
        break
    
    elif user_input.lower() == 'who':
        print(f"Current personality: {personality['emoji']} {personality['name']}")
        print(f"Temperature: {personality['temperature']}")
        continue
    
    elif user_input.lower() == 'switch':
        print("\nChoose personality:")
        for key, p in personalities.items():
            print(f"  {p['emoji']} {key}: {p['name']}")
        
        choice = input("Your choice: ").lower()
        
        if choice in personalities:
            current = choice
            personality = personalities[current]
            # Update system message
            conversation = [
                {"role": "system", "content": personality["system_message"]}
            ]
            print(f"✨ Switched to {personality['emoji']} {personality['name']}")
        else:
            print("Invalid choice")
        continue
    
    # Regular message
    conversation.append({"role": "user", "content": user_input})
    
    # Keep conversation manageable
    if len(conversation) > 10:
        conversation = [conversation[0]] + conversation[-9:]
    
    # Get response with personality's temperature
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=personality["temperature"]
    )
    
    ai_response = response.choices[0].message.content
    print(f"\n{personality['name']}: {ai_response}")
    
    # Add to conversation
    conversation.append({"role": "assistant", "content": ai_response})

print("\n🎉 Thanks for trying different personalities!")
