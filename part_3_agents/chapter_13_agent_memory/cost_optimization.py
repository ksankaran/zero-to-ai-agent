# From: AI Agents Book - Chapter 13, Section 13.7
# File: cost_optimization.py


class CostOptimizedVectorMemory:
    """Only create embeddings for important messages to save costs."""
    
    def __init__(self, collection, important_threshold=0.7):
        self.collection = collection
        self.important_threshold = important_threshold
        self.vectorized_count = 0
        self.skipped_count = 0
    
    def should_store_vector(self, message):
        """Decide if message is important enough to vectorize."""
        # Skip very short messages
        if len(message) < 10:
            return False
        
        # Skip routine responses
        routine_phrases = ["ok", "thanks", "bye", "hello", "hi", "yes", "no"]
        if message.lower().strip() in routine_phrases:
            return False
        
        # Skip if mostly punctuation
        alpha_ratio = sum(c.isalpha() for c in message) / max(len(message), 1)
        if alpha_ratio < 0.5:
            return False
        
        return True
    
    def add_message(self, message, metadata=None):
        """Only create embeddings for important messages."""
        if self.should_store_vector(message):
            # Create embedding and store (costs money)
            self.collection.add(
                documents=[message],
                metadatas=[metadata or {}],
                ids=[f"msg_{self.vectorized_count}"]
            )
            self.vectorized_count += 1
            return True
        else:
            # Skip - store in cheaper text-only storage if needed
            self.skipped_count += 1
            return False
    
    def get_stats(self):
        """Get cost optimization statistics."""
        total = self.vectorized_count + self.skipped_count
        savings = self.skipped_count / total if total > 0 else 0
        return {
            "vectorized": self.vectorized_count,
            "skipped": self.skipped_count,
            "savings_rate": f"{savings:.2%}"
        }


# Usage
if __name__ == "__main__":
    # Mock collection for demo
    class MockCollection:
        def add(self, documents, metadatas, ids):
            print(f"  Stored: {documents[0][:50]}...")
    
    memory = CostOptimizedVectorMemory(MockCollection())
    
    test_messages = [
        "hi",  # Skip
        "thanks",  # Skip
        "Can you explain how machine learning algorithms work?",  # Store
        "ok",  # Skip
        "I need help planning my project timeline for Q2",  # Store
        "bye",  # Skip
    ]
    
    print("Processing messages:")
    for msg in test_messages:
        stored = memory.add_message(msg)
        status = "STORED" if stored else "SKIPPED"
        print(f"  [{status}] {msg[:40]}...")
    
    print(f"\nStats: {memory.get_stats()}")
