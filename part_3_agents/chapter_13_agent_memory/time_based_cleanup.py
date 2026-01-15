# From: AI Agents Book - Chapter 13, Section 13.7
# File: time_based_cleanup.py

from datetime import datetime, timedelta


class TimeBasedCleanup:
    """Delete conversations older than N days."""
    
    def __init__(self, max_age_days=30):
        self.max_age_days = max_age_days
        self.conversations = {}  # session_id -> (timestamp, messages)
    
    def add_conversation(self, session_id, messages):
        """Add a conversation with current timestamp."""
        self.conversations[session_id] = (datetime.now(), messages)
    
    def cleanup(self):
        """Remove conversations older than max_age_days."""
        cutoff = datetime.now() - timedelta(days=self.max_age_days)
        
        old_sessions = [
            sid for sid, (timestamp, _) in self.conversations.items()
            if timestamp < cutoff
        ]
        
        for sid in old_sessions:
            del self.conversations[sid]
        
        return len(old_sessions)
    
    def get_conversation(self, session_id):
        """Get conversation if it exists."""
        if session_id in self.conversations:
            return self.conversations[session_id][1]
        return None


# Usage
if __name__ == "__main__":
    cleanup = TimeBasedCleanup(max_age_days=7)
    
    # Add some test conversations
    cleanup.add_conversation("user_1", ["Hello", "Hi there!"])
    cleanup.add_conversation("user_2", ["What's the weather?", "It's sunny!"])
    
    # Simulate cleanup
    deleted = cleanup.cleanup()
    print(f"Removed {deleted} old conversations")
    print(f"Remaining: {len(cleanup.conversations)} conversations")
