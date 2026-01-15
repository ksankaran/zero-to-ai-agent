# From: Zero to AI Agent, Chapter 8, Section 8.6
# File: conversation_manager.py

import json
from pathlib import Path
from datetime import datetime

class ConversationManager:
    """Manage conversation history like a pro"""
    
    def __init__(self, storage_dir="my_conversations"):
        """Set up our conversation storage system"""
        # Create a dedicated directory for conversations
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        # Track current conversation
        self.current_conversation = []
        self.conversation_metadata = {}
        
        print(f"📁 Conversation storage initialized in '{storage_dir}/'")
    
    def start_new_conversation(self, title=None):
        """Start a fresh conversation"""
        # Save previous conversation if it exists
        if self.current_conversation:
            self.save_current_conversation()
        
        # Reset for new conversation
        self.current_conversation = []
        self.conversation_metadata = {
            'id': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'title': title or f"Chat {datetime.now().strftime('%I:%M %p')}",
            'started': datetime.now().isoformat()
        }
        
        print(f"💬 Started new conversation: {self.conversation_metadata['title']}")
        return self.conversation_metadata['id']
    
    def add_message(self, role, content):
        """Add a message to the current conversation"""
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        self.current_conversation.append(message)
        
        # Auto-save every 10 messages
        if len(self.current_conversation) % 10 == 0:
            self.save_current_conversation()
            print("💾 Auto-saved (10 messages reached)")
    
    def save_current_conversation(self):
        """Save the current conversation"""
        if not self.current_conversation:
            return None
        
        # Update metadata
        self.conversation_metadata['ended'] = datetime.now().isoformat()
        self.conversation_metadata['message_count'] = len(self.current_conversation)
        
        # Create filename using ID
        conv_id = self.conversation_metadata['id']
        filename = self.storage_dir / f"conversation_{conv_id}.json"
        
        # Save everything
        data = {
            'metadata': self.conversation_metadata,
            'messages': self.current_conversation
        }
        
        print(f"dumping to {filename}")

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 Saved: {self.conversation_metadata['title']}")
        return filename
