# From: AI Agents Book - Chapter 13, Section 13.7
# File: importance_based_cleanup.py


class ImportanceBasedMemory:
    """Keep important conversations, discard routine ones."""
    
    def __init__(self):
        self.conversations = {}
    
    def add_conversation(self, conv_id, conversation):
        """Add a conversation."""
        self.conversations[conv_id] = conversation
    
    def calculate_importance(self, conversation):
        """Score conversation importance based on multiple factors."""
        score = 0
        
        # Long conversations are more important
        score += min(len(conversation.get("messages", [])), 10)
        
        # User-marked favorites
        if conversation.get("is_favorite"):
            score += 20
        
        # Contains entities (people, projects mentioned)
        score += len(conversation.get("entities", [])) * 2
        
        # Tool usage indicates complex task
        score += len(conversation.get("tool_calls", [])) * 3
        
        # Has summary (indicates substantial conversation)
        if conversation.get("summary"):
            score += 5
        
        return score
    
    def cleanup_low_importance(self, threshold=5):
        """Remove conversations below importance threshold."""
        to_delete = []
        
        for conv_id, conv in self.conversations.items():
            if self.calculate_importance(conv) < threshold:
                to_delete.append(conv_id)
        
        for conv_id in to_delete:
            del self.conversations[conv_id]
        
        return len(to_delete)
    
    def get_important_conversations(self, min_importance=10):
        """Get conversations above importance threshold."""
        return {
            conv_id: conv 
            for conv_id, conv in self.conversations.items()
            if self.calculate_importance(conv) >= min_importance
        }


# Usage
if __name__ == "__main__":
    memory = ImportanceBasedMemory()
    
    # Add conversations with different importance levels
    memory.add_conversation("conv_1", {
        "messages": ["hi", "bye"],
        "entities": [],
        "tool_calls": []
    })
    
    memory.add_conversation("conv_2", {
        "messages": ["Tell me about Project Alpha", "What's the status?", "Update the timeline"],
        "entities": ["Project Alpha", "Sarah"],
        "tool_calls": ["search", "calendar"],
        "is_favorite": True
    })
    
    # Show importance scores
    for conv_id, conv in memory.conversations.items():
        score = memory.calculate_importance(conv)
        print(f"{conv_id}: importance = {score}")
    
    # Cleanup low importance
    deleted = memory.cleanup_low_importance(threshold=5)
    print(f"\nDeleted {deleted} low-importance conversations")
    print(f"Remaining: {list(memory.conversations.keys())}")
