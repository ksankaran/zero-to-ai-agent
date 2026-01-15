# From: Zero to AI Agent, Chapter 3, Section 3.5
# simple_chatbot.py

print("ChatBot: Hello! I'm a simple AI assistant. Type 'bye' to exit.")

chatting = True
while chatting:
    user_input = input("\nYou: ").lower()
    
    if user_input == "bye":
        chatting = False
        print("ChatBot: Goodbye! Have a great day!")
    elif user_input == "hello" or user_input == "hi":
        print("ChatBot: Hello there! How can I help you?")
    elif "weather" in user_input:
        print("ChatBot: I'm sorry, I don't have weather data. I'm still learning!")
    elif "your name" in user_input:
        print("ChatBot: I'm ChatBot, your friendly AI assistant!")
    else:
        print("ChatBot: That's interesting! Tell me more.")
