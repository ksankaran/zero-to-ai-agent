# From: Zero to AI Agent, Chapter 8, Section 8.6
# File: searchable_history.py

import json
from pathlib import Path

def search_conversations(search_term, storage_dir="my_conversations"):
    """Search through all saved conversations"""
    storage_path = Path(storage_dir)
    results = []
    search_lower = search_term.lower()
    
    print(f"🔍 Searching for '{search_term}'...")
    
    # Check if directory exists
    if not storage_path.exists():
        print(f"❌ Directory {storage_dir} doesn't exist!")
        return []
    
    # Search through each conversation file
    for conv_file in storage_path.glob("conversation_*.json"):
        try:
            with open(conv_file, 'r') as f:
                data = json.load(f)
            
            # Search in messages
            for msg in data.get('messages', []):
                if search_lower in msg.get('content', '').lower():
                    # Found a match!
                    metadata = data.get('metadata', {})
                    results.append({
                        'file': conv_file.name,
                        'title': metadata.get('title', 'Untitled'),
                        'date': metadata.get('started', data.get('saved_at', 'Unknown')),
                        'preview': msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content'],
                        'role': msg['role'],
                        'full_path': str(conv_file)
                    })
                    break  # One result per conversation
        except Exception as e:
            print(f"⚠️ Error reading {conv_file.name}: {e}")
            continue
    
    # Display results
    if results:
        print(f"\n✅ Found {len(results)} conversations containing '{search_term}':\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   Date: {result['date'][:19] if len(result['date']) > 19 else result['date']}")
            print(f"   Preview: {result['preview']}")
            print(f"   File: {result['file']}")
            print()
    else:
        print(f"❌ No conversations found containing '{search_term}'")
    
    return results

def search_advanced(storage_dir="my_conversations", **criteria):
    """Advanced search with multiple criteria"""
    storage_path = Path(storage_dir)
    results = []
    
    # Search criteria
    search_term = criteria.get('term', '').lower()
    role_filter = criteria.get('role', None)  # 'user' or 'assistant'
    date_from = criteria.get('date_from', None)
    date_to = criteria.get('date_to', None)
    min_messages = criteria.get('min_messages', 0)
    
    if not storage_path.exists():
        return []
    
    for conv_file in storage_path.glob("conversation_*.json"):
        try:
            with open(conv_file, 'r') as f:
                data = json.load(f)
            
            # Check message count
            if len(data.get('messages', [])) < min_messages:
                continue
            
            # Check date range if specified
            if date_from or date_to:
                conv_date = data.get('saved_at', data.get('metadata', {}).get('started', ''))
                if date_from and conv_date < date_from:
                    continue
                if date_to and conv_date > date_to:
                    continue
            
            # Search in messages
            for msg in data.get('messages', []):
                # Check role filter
                if role_filter and msg.get('role') != role_filter:
                    continue
                
                # Check search term
                if search_term and search_term not in msg.get('content', '').lower():
                    continue
                
                # Match found!
                metadata = data.get('metadata', {})
                results.append({
                    'file': conv_file.name,
                    'title': metadata.get('title', 'Untitled'),
                    'date': metadata.get('started', data.get('saved_at', 'Unknown')),
                    'preview': msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content'],
                    'role': msg['role'],
                    'message_count': len(data.get('messages', [])),
                    'full_path': str(conv_file)
                })
                break
                
        except Exception as e:
            continue
    
    return results

def load_conversation_for_viewing(filepath):
    """Load a specific conversation for viewing"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        print(f"\n📂 Loading: {Path(filepath).name}")
        print("=" * 50)
        
        # Show metadata
        metadata = data.get('metadata', {})
        print(f"Title: {metadata.get('title', 'Untitled')}")
        print(f"Started: {metadata.get('started', 'Unknown')}")
        print(f"Messages: {len(data.get('messages', []))}")
        print("-" * 50)
        
        # Show messages
        for msg in data.get('messages', []):
            role = "YOU" if msg['role'] == 'user' else "AI"
            print(f"\n{role}:")
            print(msg['content'])
            print("-" * 40)
        
        return data
        
    except Exception as e:
        print(f"❌ Error loading conversation: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Simple search
    print("🔍 Simple Search Demo")
    print("=" * 50)
    results = search_conversations("python")
    
    # Advanced search
    print("\n🔍 Advanced Search Demo")
    print("=" * 50)
    advanced_results = search_advanced(
        term="code",
        role="assistant",
        min_messages=5
    )
    
    if advanced_results:
        print(f"Found {len(advanced_results)} conversations with advanced criteria")
        for result in advanced_results[:3]:  # Show first 3
            print(f"- {result['title']} ({result['message_count']} messages)")
    
    # Load and view a specific conversation
    if results:
        print("\n📖 Loading first search result...")
        load_conversation_for_viewing(results[0]['full_path'])