# From: Zero to AI Agent, Chapter 4, Section 4.2
# memory_system.py - Simple conversation memory system for AI agents

# Simple conversation memory system using dictionaries and lists
# No classes or functions - just direct manipulation

# Initialize our memory system
memory = {
    "conversations": [],
    "max_size": 5,
    "important_messages": [],
    "message_count": 0
}

print("Memory system initialized")
print(f"Max conversation size: {memory['max_size']}")

# Simulate adding messages
messages_to_add = [
    "User: Hello AI!",
    "AI: Hello! How can I help you?",
    "User: Tell me about Python lists",
    "AI: Lists are ordered collections in Python",
    "User: How do I add items?",
    "AI: Use append() to add items to a list",
    "User: Thanks, that's helpful!"
]

print("\nAdding messages to memory:")
for msg in messages_to_add:
    # Add message to conversations
    memory["conversations"].append(msg)
    memory["message_count"] += 1
    
    # Check if we exceeded max size (sliding window)
    if len(memory["conversations"]) > memory["max_size"]:
        removed = memory["conversations"].pop(0)  # Remove oldest
        print(f"  Memory full, removed: {removed}")
    
    print(f"  Added: {msg}")

print(f"\nCurrent memory state:")
print(f"  Total messages processed: {memory['message_count']}")
print(f"  Messages in memory: {len(memory['conversations'])}")

# Get recent context (last 3 messages)
context_size = 3
if len(memory["conversations"]) >= context_size:
    recent_context = memory["conversations"][-context_size:]
else:
    recent_context = memory["conversations"].copy()

print(f"\nRecent context ({len(recent_context)} messages):")
for msg in recent_context:
    print(f"  {msg}")

# Mark important messages
important_keywords = ["thanks", "helpful", "great"]
for msg in memory["conversations"]:
    msg_lower = msg.lower()
    for keyword in important_keywords:
        if keyword in msg_lower and msg not in memory["important_messages"]:
            memory["important_messages"].append(msg)
            print(f"\nMarked as important: {msg}")
            break

# Search for specific keywords
search_term = "list"
print(f"\nSearching for messages containing '{search_term}':")
found_messages = []
for msg in memory["conversations"]:
    if search_term.lower() in msg.lower():
        found_messages.append(msg)
        print(f"  Found: {msg}")

print(f"\nTotal matches: {len(found_messages)}")

# Summary statistics
print("\n=== Memory Summary ===")
print(f"Messages in memory: {len(memory['conversations'])}")
print(f"Important messages: {len(memory['important_messages'])}")
print(f"Total processed: {memory['message_count']}")
if memory["conversations"]:
    print(f"Oldest message: {memory['conversations'][0]}")
    print(f"Latest message: {memory['conversations'][-1]}")
