# From: Zero to AI Agent, Chapter 5, Section 5.1
# File: simple_chatbot.py
# Topic: Functions are everywhere in AI systems

def process_user_message():
    """Get and clean up user input"""
    message = input("You: ")
    # In real AI: clean, tokenize, prepare the message
    return message

def generate_ai_response():
    """Create an AI response"""
    # In real AI: call the language model API
    response = "I'm a simple bot. In later chapters, I'll be much smarter!"
    return response

def display_response():
    """Show the response to user"""
    response = generate_ai_response()
    print(f"AI: {response}")

def run_chatbot():
    """Main chatbot function"""
    print("Simple Chatbot v0.1")
    print("This is just a skeleton - we'll add AI later!")
    print("-" * 40)
    
    process_user_message()
    display_response()

# Run our (very simple) chatbot
run_chatbot()
