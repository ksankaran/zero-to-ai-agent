# From: Zero to AI Agent, Chapter 5, Section 5.7
# File: ai_assistant.py

# file: ai_assistant.py
"""
A simple AI assistant module for demonstration.
This will be enhanced with real AI in later chapters!
"""

import random
from datetime import datetime

class SimpleAssistant:
    """A basic assistant that will become AI-powered later"""
    
    def __init__(self, name="Assistant"):
        self.name = name
        self.creation_time = datetime.now()
        self.conversation_count = 0
        
    def greet(self):
        """Generate a greeting"""
        greetings = [
            f"Hello! I'm {self.name}, your assistant.",
            f"Hi there! {self.name} at your service!",
            f"Greetings! I'm {self.name}, how can I help?"
        ]
        return random.choice(greetings)
    
    def respond(self, user_input):
        """Generate a response (will use AI later!)"""
        self.conversation_count += 1
        
        # Simple keyword-based responses for now
        user_input_lower = user_input.lower()
        
        if "hello" in user_input_lower or "hi" in user_input_lower:
            return "Hello! How are you doing today?"
        elif "time" in user_input_lower:
            current_time = datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}"
        elif "name" in user_input_lower:
            return f"My name is {self.name}"
        elif "bye" in user_input_lower:
            return "Goodbye! Have a great day!"
        else:
            return "That's interesting! Tell me more."
    
    def get_stats(self):
        """Return conversation statistics"""
        uptime = datetime.now() - self.creation_time
        return {
            "name": self.name,
            "conversations": self.conversation_count,
            "uptime_seconds": uptime.total_seconds()
        }

# Helper functions
def create_assistant(name="AI"):
    """Factory function to create an assistant"""
    return SimpleAssistant(name)

def format_stats(stats):
    """Format statistics nicely"""
    return f"""
    Assistant Statistics:
    Name: {stats['name']}
    Conversations: {stats['conversations']}
    Uptime: {stats['uptime_seconds']:.1f} seconds
    """

# Module info
VERSION = "2.0.0"
CAPABILITIES = ["greeting", "time", "basic chat"]

if __name__ == "__main__":
    # Demo when run directly
    print("AI Assistant Module Demo")
    print("-" * 40)
    
    assistant = create_assistant("Demo Bot")
    print(assistant.greet())
    
    response = assistant.respond("What time is it?")
    print(f"User: What time is it?")
    print(f"Bot: {response}")
    
    stats = assistant.get_stats()
    print(format_stats(stats))