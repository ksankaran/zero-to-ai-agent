# From: Zero to AI Agent, Chapter 8, Section 8.5
# File: complete_chat.py

from smart_chatbot import SmartChatBot
from commands import CommandHandler
from personalities import get_personality
from api_helper import get_client

def main():
    # Setup
    client = get_client()
    bot = SmartChatBot(client, max_context=10)
    
    # Add command handling
    cmd_handler = CommandHandler()
    cmd_handler.set_bot(bot)
    
    print("🤖 Complete Modular Chatbot")
    print("Type /help for commands, 'quit' to exit")
    print("-" * 40)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            break
        
        # Check for commands
        cmd_response = cmd_handler.handle(user_input)
        if cmd_response:
            print(f"\n{cmd_response}")
            continue
        
        # Regular chat
        response = bot.chat(user_input)
        print(f"Bot: {response}")
        
        # Show truncation warning if needed
        stats = bot.get_stats()
        if stats['truncated']:
            print(f"[Context limited to last {stats['context_size']} messages]")

if __name__ == "__main__":
    main()
