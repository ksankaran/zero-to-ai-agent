# From: AI Agents Book - Chapter 13, Section 13.2
# File: conversation_manager.py

from conversation_memory import ConversationMemory

class ConversationManager:
    def __init__(self, system_prompt=None):
        self.conversations = {}  # user_id -> ConversationMemory
        self.system_prompt = system_prompt
    
    def get_or_create(self, user_id):
        """Get existing conversation or create new one."""
        if user_id not in self.conversations:
            self.conversations[user_id] = ConversationMemory(
                system_prompt=self.system_prompt
            )
        return self.conversations[user_id]
    
    def chat(self, user_id, message):
        """Chat with a specific user's conversation."""
        memory = self.get_or_create(user_id)
        return memory.chat(message)
    
    def clear_conversation(self, user_id):
        """Clear a specific user's history."""
        if user_id in self.conversations:
            self.conversations[user_id].clear()


# Example usage
if __name__ == "__main__":
    manager = ConversationManager(system_prompt="You are a helpful assistant.")

    # Different users, different conversations
    manager.chat("user_123", "My name is Alice")
    manager.chat("user_456", "My name is Bob")

    print(manager.chat("user_123", "What's my name?"))  # "Alice"
    print(manager.chat("user_456", "What's my name?"))  # "Bob"
