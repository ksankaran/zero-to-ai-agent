# From: AI Agents Book - Chapter 13, Section 13.2
# File: persistent_memory.py

import json
from pathlib import Path
from conversation_memory import ConversationMemory

class PersistentConversationMemory(ConversationMemory):
    def __init__(self, user_id, storage_dir="conversations", **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.storage_path = Path(storage_dir) / f"{user_id}.json"
        self.storage_path.parent.mkdir(exist_ok=True)
        self._load()
    
    def _load(self):
        """Load conversation from disk if it exists."""
        if self.storage_path.exists():
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                self.messages = data.get("messages", [])
    
    def _save(self):
        """Save conversation to disk."""
        with open(self.storage_path, 'w') as f:
            json.dump({"messages": self.messages}, f, indent=2)
    
    def add_user_message(self, content):
        super().add_user_message(content)
        self._save()
    
    def add_assistant_message(self, content):
        super().add_assistant_message(content)
        self._save()


# Example usage
if __name__ == "__main__":
    # First run - creates new conversation
    memory = PersistentConversationMemory(
        user_id="alice",
        system_prompt="You are a helpful assistant."
    )
    
    print(memory.chat("Hi! I'm planning a vacation."))
    print(f"Saved to: {memory.storage_path}")
    
    # Second run - would load existing conversation
    # memory2 = PersistentConversationMemory(user_id="alice")
    # print(memory2.chat("What was I planning?"))  # It remembers!
