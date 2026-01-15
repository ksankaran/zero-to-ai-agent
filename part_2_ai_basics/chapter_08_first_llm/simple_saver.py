# From: Zero to AI Agent, Chapter 8, Section 8.6
# File: simple_saver.py

import json
from datetime import datetime
from pathlib import Path

def save_conversation(messages, filename=None):
    """Save a conversation to a JSON file"""
    # Auto-generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.json"
    
    # Create the data structure
    conversation_data = {
        "saved_at": datetime.now().isoformat(),
        "message_count": len(messages),
        "messages": messages
    }
    
    # Save to file
    with open(filename, 'w') as f:
        json.dump(conversation_data, f, indent=2)
    
    print(f"💾 Conversation saved to {filename}")
    return filename

# Example usage
sample_conversation = [
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a high-level programming language..."},
    {"role": "user", "content": "Show me an example"},
    {"role": "assistant", "content": "Here's a simple example: print('Hello, World!')"}
]

# Save it!
save_conversation(sample_conversation)
