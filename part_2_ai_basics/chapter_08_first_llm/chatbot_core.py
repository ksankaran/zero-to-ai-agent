# From: Zero to AI Agent, Chapter 8, Section 8.5
# File: chatbot_core.py

"""Core chatbot functionality - keep it simple and reusable!"""

class ChatBot:
    """Basic chatbot that maintains conversation context"""
    
    def __init__(self, client, system_message="You are a helpful assistant."):
        self.client = client
        self.messages = [{"role": "system", "content": system_message}]
    
    def chat(self, user_message):
        """Send a message and get a response"""
        # Add user message to history
        self.messages.append({"role": "user", "content": user_message})
        
        # Get AI response
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        
        # Extract and store AI message
        ai_message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": ai_message})
        
        return ai_message
    
    def reset(self):
        """Reset conversation, keep system message"""
        self.messages = self.messages[:1]
