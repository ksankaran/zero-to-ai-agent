# From: Zero to AI Agent, Chapter 8, Section 8.5
# File: simple_chat.py

from chatbot_core import ChatBot
from api_helper import get_client

def main():
    # Setup
    client = get_client()
    bot = ChatBot(client)
    
    print("💬 Simple Chatbot")
    print("Type 'quit' to exit, 'reset' to start over")
    print("-" * 40)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'reset':
            bot.reset()
            print("🔄 Conversation reset!")
            continue
        
        response = bot.chat(user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
