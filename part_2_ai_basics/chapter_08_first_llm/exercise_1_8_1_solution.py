# From: Zero to AI Agent, Chapter 8, Section 8.1
# File: exercise_1_8_1_personality_bot.py

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

# Setup
api_key = load_api_key()
if not api_key:
    print("❌ No API key found! Run setup_api_key.py first!")
    exit()

client = openai.OpenAI(api_key=api_key)

# Define personalities
personalities = {
    "pirate": "You are a friendly pirate. Speak with pirate slang, say 'arr' and 'matey' often, and reference the sea, treasure, and ships in your responses.",
    "chef": "You are a passionate French chef. Use cooking metaphors, occasionally use French words, and relate everything to food and cooking.",
    "poet": "You are a romantic poet. Speak in a lyrical, flowery manner. Sometimes respond in rhyme or verse. Reference nature and emotions.",
    "robot": "You are a helpful robot. Use technical language, be very logical, occasionally say 'BEEP BOOP', and reference your circuits and processors."
}

# Start with default personality
current_personality = "pirate"
conversation = [
    {"role": "system", "content": personalities[current_personality]}
]

print("🎭 Personality Bot!")
print(f"Current personality: {current_personality.upper()}")
print("Commands: 'quit', 'switch' to change personality")
print("-" * 40)

while True:
    user_message = input("\nYou: ")
    
    if user_message.lower() == 'quit':
        print("👋 Farewell! Thanks for the chat!")
        break
    
    if user_message.lower() == 'switch':
        print("\nAvailable personalities:")
        for i, p in enumerate(personalities.keys(), 1):
            print(f"  {i}. {p}")
        
        choice = input("Choose personality (number): ")
        try:
            personality_list = list(personalities.keys())
            idx = int(choice) - 1
            if 0 <= idx < len(personality_list):
                current_personality = personality_list[idx]
                # Reset conversation with new personality
                conversation = [
                    {"role": "system", "content": personalities[current_personality]}
                ]
                print(f"✨ Switched to {current_personality} personality!")
        except:
            print("Invalid choice, keeping current personality")
        continue
    
    # Add user message
    conversation.append({"role": "user", "content": user_message})
    
    # Get AI response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.9  # Higher temperature for more creative personalities!
    )
    
    ai_message = response.choices[0].message.content
    print(f"\n{current_personality.upper()}: {ai_message}")
    
    # Add to conversation history
    conversation.append({"role": "assistant", "content": ai_message})
    
    # Keep conversation manageable
    if len(conversation) > 10:
        conversation = [conversation[0]] + conversation[-9:]

print("\n🎭 Thanks for trying different personalities!")
