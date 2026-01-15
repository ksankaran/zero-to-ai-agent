# From: Zero to AI Agent, Chapter 8, Section 8.5
# File: smart_chatbot.py

"""Smarter chatbot with memory management"""

from memory_manager import MemoryManager

class SmartChatBot:
    """Chatbot with intelligent memory management"""
    
    def __init__(self, client, system_message="You are a helpful assistant.", max_context=20):
        self.client = client
        self.system_message = {"role": "system", "content": system_message}
        self.messages = [self.system_message]
        self.memory = MemoryManager(max_context)
    
    def chat(self, user_message):
        """Chat with smart context management"""
        # Add user message
        self.messages.append({"role": "user", "content": user_message})
        
        # Get context window for API call
        context = self.memory.get_context(self.messages)
        
        # Make API call with managed context
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=context
        )
        
        # Store response
        ai_message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": ai_message})
        
        return ai_message
    
    def get_stats(self):
        """Get conversation statistics"""
        return {
            "total_messages": len(self.messages) - 1,  # Exclude system
            "context_size": len(self.memory.get_context(self.messages)),
            "truncated": self.memory.should_truncate(self.messages)
        }
