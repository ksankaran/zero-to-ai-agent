# From: Zero to AI Agent, Chapter 4, Section 4.4
# dict_modifying.py - Adding, updating, and removing dictionary items

# Starting with a basic AI agent state
agent_state = {
    "status": "idle",
    "messages_processed": 0,
    "last_active": None
}

print("Initial state:", agent_state)

# Adding new key-value pairs
agent_state["model"] = "gpt-3.5-turbo"
agent_state["context"] = []
print("\nAfter adding keys:", agent_state)

# Updating existing values
agent_state["status"] = "active"
agent_state["messages_processed"] += 1
agent_state["last_active"] = "2024-01-15 10:30:00"
print("\nAfter updates:", agent_state)

# Update multiple values at once
updates = {
    "status": "processing",
    "messages_processed": 5,
    "error_count": 0  # This adds a new key too!
}
agent_state.update(updates)
print("\nAfter batch update:", agent_state)

# Removing items
del agent_state["error_count"]  # Remove using del
removed = agent_state.pop("last_active", None)  # Remove and return value
print(f"\nRemoved last_active: {removed}")
print("State after removals:", agent_state)

# Clear everything
# agent_state.clear()  # Empties the dictionary
