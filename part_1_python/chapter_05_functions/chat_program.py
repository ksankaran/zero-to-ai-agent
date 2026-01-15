# From: Zero to AI Agent, Chapter 5, Section 5.7
# File: chat_program.py

# file: chat_program.py
from ai_assistant import create_assistant, format_stats

# Create your assistant
bot = create_assistant("PyBot")
print(bot.greet())
print("-" * 40)

# Have a conversation
while True:
    user_input = input("You: ")
    if user_input.lower() in ['quit', 'exit', 'bye']:
        print(bot.respond(user_input))
        break
    
    response = bot.respond(user_input)
    print(f"PyBot: {response}")

# Show statistics
print("\nSession Statistics:")
print(format_stats(bot.get_stats()))