# From: Zero to AI Agent, Chapter 5, Section 5.8
# conversation_class.py - AI-ready conversation management class

class Conversation:
    """Manages a conversation history - useful for AI chatbots!"""

    def __init__(self, system_prompt="You are a helpful assistant."):
        self.system_prompt = system_prompt
        self.messages = []

    def add_user_message(self, content):
        """Add a message from the user"""
        self.messages.append({
            "role": "user",
            "content": content
        })

    def add_assistant_message(self, content):
        """Add a message from the assistant"""
        self.messages.append({
            "role": "assistant",
            "content": content
        })

    def get_message_count(self):
        """Return total number of messages"""
        return len(self.messages)

    def get_last_message(self):
        """Get the most recent message"""
        if self.messages:
            return self.messages[-1]
        return None

    def clear(self):
        """Clear conversation history"""
        self.messages = []
        print("Conversation cleared!")


# Using the conversation class
chat = Conversation("You are a Python tutor.")

chat.add_user_message("What is a class?")
chat.add_assistant_message("A class is a blueprint for creating objects...")

print(f"Messages: {chat.get_message_count()}")
print(f"Last message: {chat.get_last_message()}")
