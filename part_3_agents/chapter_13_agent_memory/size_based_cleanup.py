# From: AI Agents Book - Chapter 13, Section 13.7
# File: size_based_cleanup.py

from collections import deque


class SizeBasedMemory:
    """Keep only the N most recent conversations per user."""
    
    def __init__(self, max_conversations_per_user=10):
        self.max_conversations = max_conversations_per_user
        self.user_conversations = {}  # user_id -> deque of conversations
    
    def add_conversation(self, user_id, conversation):
        """Add conversation, automatically dropping oldest when full."""
        if user_id not in self.user_conversations:
            self.user_conversations[user_id] = deque(maxlen=self.max_conversations)
        
        # Automatically drops oldest when full
        self.user_conversations[user_id].append(conversation)
    
    def get_recent_conversations(self, user_id, n=5):
        """Return n most recent conversations for user."""
        if user_id not in self.user_conversations:
            return []
        
        # Return n most recent
        return list(self.user_conversations[user_id])[-n:]
    
    def get_all_conversations(self, user_id):
        """Get all stored conversations for user."""
        if user_id not in self.user_conversations:
            return []
        return list(self.user_conversations[user_id])
    
    def get_conversation_count(self, user_id):
        """Get number of stored conversations for user."""
        if user_id not in self.user_conversations:
            return 0
        return len(self.user_conversations[user_id])


# Usage
if __name__ == "__main__":
    memory = SizeBasedMemory(max_conversations_per_user=3)
    
    # Add conversations for user
    for i in range(5):
        memory.add_conversation("user_123", {"id": i, "messages": [f"Conversation {i}"]})
    
    # Only 3 most recent are kept
    conversations = memory.get_all_conversations("user_123")
    print(f"Stored {len(conversations)} conversations (max 3)")
    for conv in conversations:
        print(f"  - {conv}")
