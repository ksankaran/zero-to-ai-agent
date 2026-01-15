# From: Zero to AI Agent, Chapter 8, Section 8.5
# File: memory_manager.py

"""Manage conversation memory intelligently"""

class MemoryManager:
    """Manage conversation context window"""
    
    def __init__(self, max_messages=20):
        self.max_messages = max_messages
    
    def get_context(self, messages):
        """Get messages that fit in context window"""
        if len(messages) <= self.max_messages:
            return messages
        
        # Always keep system message + recent messages
        return [messages[0]] + messages[-(self.max_messages-1):]
    
    def should_truncate(self, messages):
        """Check if truncation is needed"""
        return len(messages) > self.max_messages
