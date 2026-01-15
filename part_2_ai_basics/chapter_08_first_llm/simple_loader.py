# From: Zero to AI Agent, Chapter 8, Section 8.6
# File: simple_loader.py

import json
from pathlib import Path

def load_conversation(filename):
    """Load a conversation from a JSON file"""
    file_path = Path(filename)
    
    # Check if file exists
    if not file_path.exists():
        print(f"❌ File {filename} not found!")
        return None
    
    # Load the data
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    print(f"✅ Loaded {data['message_count']} messages")
    print(f"📅 Saved on: {data['saved_at']}")
    
    return data['messages']

def list_saved_conversations():
    """Find all saved conversation files"""
    # Look for conversation files
    files = list(Path(".").glob("conversation_*.json"))
    
    if not files:
        print("No saved conversations found!")
        return []
    
    print(f"\n📚 Found {len(files)} saved conversations:")
    for i, file in enumerate(files, 1):
        # Get file info
        size = file.stat().st_size / 1024  # Size in KB
        modified = datetime.fromtimestamp(file.stat().st_mtime)
        
        print(f"  {i}. {file.name}")
        print(f"     Size: {size:.1f} KB")
        print(f"     Modified: {modified.strftime('%Y-%m-%d %H:%M')}")
    
    return files

# Try it out
files = list_saved_conversations()
if files:
    # Load the first one
    messages = load_conversation(files[0])
