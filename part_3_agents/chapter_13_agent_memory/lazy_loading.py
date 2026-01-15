# From: AI Agents Book - Chapter 13, Section 13.7
# File: lazy_loading.py

from dotenv import load_dotenv
load_dotenv()

from langchain_community.chat_message_histories import SQLChatMessageHistory


class LazyLoadMemory:
    """Don't load entire conversation history upfront."""
    
    def __init__(self, session_id, db_path):
        self.session_id = session_id
        self.db_path = db_path
        self._messages = None  # Not loaded yet
        self._loaded = False
    
    @property
    def messages(self):
        """Load messages only when accessed."""
        if self._messages is None:
            self._messages = self._load_messages()
            self._loaded = True
        return self._messages
    
    def _load_messages(self):
        """Load from database."""
        history = SQLChatMessageHistory(
            session_id=self.session_id,
            connection=self.db_path
        )
        return history.messages
    
    def get_recent(self, n=10):
        """Get only recent messages without loading all."""
        # For efficiency, could implement a direct DB query
        # This is a simplified version
        return self.messages[-n:] if self.messages else []
    
    def is_loaded(self):
        """Check if messages have been loaded."""
        return self._loaded
    
    def reload(self):
        """Force reload from database."""
        self._messages = None
        self._loaded = False
        return self.messages


# Usage
if __name__ == "__main__":
    memory = LazyLoadMemory("user_123", "sqlite:///chat.db")
    
    print(f"Loaded: {memory.is_loaded()}")  # False
    
    # Messages loaded on first access
    recent = memory.get_recent(5)
    print(f"Loaded: {memory.is_loaded()}")  # True
    print(f"Recent messages: {len(recent)}")
