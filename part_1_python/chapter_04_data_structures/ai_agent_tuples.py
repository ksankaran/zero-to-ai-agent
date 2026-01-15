# From: Zero to AI Agent, Chapter 4, Section 4.3
# ai_agent_tuples.py - Using tuples in AI agent development

# AI Agent configuration and state management using tuples and dictionaries

# Agent configuration (immutable - use tuple)
agent_config = ("Assistant", "gpt-3.5", 2048, 0.7)  # (name, model, max_tokens, temperature)
print(f"Agent Configuration: {agent_config}")
print(f"Agent name: {agent_config[0]}")
print(f"Model: {agent_config[1]}")

# Conversation state (mutable - use dictionary with lists)
conversation_state = {
    "config": agent_config,  # Store the immutable config
    "history": [],  # Mutable conversation history
    "message_count": 0,
    "context_window": 5
}

# Simulate conversation
messages = [
    ("user", "Hello!", "2024-01-15 10:30:00"),
    ("assistant", "Hi there! How can I help?", "2024-01-15 10:30:01"),
    ("user", "What's the weather?", "2024-01-15 10:30:15"),
    ("assistant", "I'll check that for you.", "2024-01-15 10:30:16")
]

print("\nProcessing messages:")
for role, content, timestamp in messages:  # Unpacking tuple
    # Each message is stored as a tuple (immutable record)
    message_record = (role, content, timestamp)
    conversation_state["history"].append(message_record)
    conversation_state["message_count"] += 1
    print(f"  Added: {role} - {content}")

# Get recent context
context_size = conversation_state["context_window"]
recent = conversation_state["history"][-context_size:]

print(f"\nRecent context ({len(recent)} messages):")
for role, content, timestamp in recent:
    print(f"  [{timestamp}] {role}: {content}")

# Statistics as a tuple (immutable snapshot)
stats = (
    conversation_state["message_count"],
    len(conversation_state["history"]),
    conversation_state["config"][0],  # Agent name
    conversation_state["config"][1]   # Model
)

messages_processed, history_length, agent_name, model_used = stats
print(f"\nStatistics Snapshot:")
print(f"  Agent: {agent_name}")
print(f"  Model: {model_used}")
print(f"  Messages processed: {messages_processed}")
print(f"  History length: {history_length}")
