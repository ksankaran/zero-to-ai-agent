# From: Zero to AI Agent, Chapter 4, Section 4.4
# conversation_memory.py - Building a memory system with dictionaries

# Conversation memory system using dictionaries
memory_system = {
    "conversations": {},  # Will store conversations by user_id
    "user_profiles": {},  # Will store user information
    "context_cache": {},  # Recent context by user
    "max_size": 10       # Maximum messages per conversation
}

# Initialize users
user_ids = ["user_123", "user_456"]
for user_id in user_ids:
    memory_system["conversations"][user_id] = []
    memory_system["user_profiles"][user_id] = {
        "name": f"User_{user_id[-3:]}",
        "first_seen": "2024-01-15",
        "message_count": 0,
        "topics": []  # Topics discussed
    }

print("Memory system initialized for users:", user_ids)

# Add messages for user_123
messages = [
    ("user", "Hello AI!", "2024-01-15 10:30:00"),
    ("assistant", "Hello! How can I help you?", "2024-01-15 10:30:01"),
    ("user", "Tell me about Python lists", "2024-01-15 10:30:15"),
    ("assistant", "Lists are ordered collections in Python", "2024-01-15 10:30:16"),
    ("user", "How do I add items?", "2024-01-15 10:30:30"),
    ("assistant", "Use append() to add items to a list", "2024-01-15 10:30:31"),
]

current_user = "user_123"
print(f"\nAdding messages for {current_user}:")

for role, content, timestamp in messages:
    # Create message record
    message = {
        "role": role,
        "content": content,
        "timestamp": timestamp,
        "tokens": len(content.split()) * 2  # Rough estimate
    }
    
    # Add to conversation
    memory_system["conversations"][current_user].append(message)
    
    # Update user profile
    if role == "user":
        memory_system["user_profiles"][current_user]["message_count"] += 1
        
        # Simple topic extraction
        if "python" in content.lower():
            if "programming" not in memory_system["user_profiles"][current_user]["topics"]:
                memory_system["user_profiles"][current_user]["topics"].append("programming")
        if "list" in content.lower():
            if "data structures" not in memory_system["user_profiles"][current_user]["topics"]:
                memory_system["user_profiles"][current_user]["topics"].append("data structures")
    
    print(f"  Added: {role} - {content[:30]}...")
    
    # Check if exceeded max size
    if len(memory_system["conversations"][current_user]) > memory_system["max_size"]:
        removed = memory_system["conversations"][current_user].pop(0)
        print(f"  Memory full! Removed oldest message")

# Get context for user
context_size = 3
user_conversation = memory_system["conversations"][current_user]
if len(user_conversation) >= context_size:
    recent_context = user_conversation[-context_size:]
else:
    recent_context = user_conversation.copy()

# Cache the context
memory_system["context_cache"][current_user] = {
    "messages": recent_context,
    "summary": f"{len(recent_context)} recent messages",
    "total_tokens": sum(m["tokens"] for m in recent_context)
}

print(f"\nContext for {current_user}:")
for msg in recent_context:
    print(f"  [{msg['timestamp']}] {msg['role']}: {msg['content'][:40]}...")

# Display user profile
profile = memory_system["user_profiles"][current_user]
print(f"\nUser Profile for {current_user}:")
print(f"  Name: {profile['name']}")
print(f"  Messages sent: {profile['message_count']}")
print(f"  Topics: {profile['topics']}")
print(f"  First seen: {profile['first_seen']}")

# Search for keywords
search_term = "list"
print(f"\nSearching for '{search_term}' in conversations:")
found_messages = []
for msg in memory_system["conversations"][current_user]:
    if search_term.lower() in msg["content"].lower():
        found_messages.append(msg)
        print(f"  Found in {msg['role']} message: {msg['content'][:50]}...")

print(f"Total matches: {len(found_messages)}")
