# From: Zero to AI Agent, Chapter 8, Section 8.5
# File: personality_chat.py

from chatbot_core import ChatBot
from api_helper import get_client
from personalities import get_personality, list_personalities

def main():
    client = get_client()
    
    # Show available personalities
    print("🎭 Choose a personality:")
    for p in list_personalities():
        print(f"  - {p}")
    
    choice = input("\nYour choice: ").strip().lower()
    personality = get_personality(choice)
    
    # Create bot with chosen personality
    bot = ChatBot(client, system_message=personality)
    
    print(f"\n💬 Chatbot with {choice} personality")
    print("Type 'quit' to exit")
    print("-" * 40)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            break
        
        response = bot.chat(user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
