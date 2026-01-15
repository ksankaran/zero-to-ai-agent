# From: Zero to AI Agent, Chapter 8, Section 8.5
# File: filtered_chat.py

from chatbot_core import ChatBot
from api_helper import get_client
from response_filters import ResponseFilter

def main():
    client = get_client()
    bot = ChatBot(client)
    filter = ResponseFilter()
    
    print("💬 Chatbot with Response Filters")
    print("Commands: 'brief', 'emoji', 'loud', 'normal'")
    print("-" * 40)
    
    filter_mode = "normal"
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() in ['brief', 'emoji', 'loud', 'normal']:
            filter_mode = user_input.lower()
            print(f"Filter set to: {filter_mode}")
            continue
        
        # Get response
        response = bot.chat(user_input)
        
        # Apply filter
        if filter_mode == 'brief':
            response = filter.make_brief(response)
        elif filter_mode == 'emoji':
            response = filter.add_emoji(response)
        elif filter_mode == 'loud':
            response = filter.make_uppercase(response)
        
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
