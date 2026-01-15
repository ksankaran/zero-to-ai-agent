# From: Zero to AI Agent, Chapter 4, Section 4.1
# ai_conversation.py - Simulating chatbot conversation history

# Simulating a simple chatbot conversation history
conversation = []  # Start with empty list

# Adding user messages (we'll learn append in the next section)
conversation = conversation + ["User: Hello!"]
conversation = conversation + ["Bot: Hi there! How can I help?"]
conversation = conversation + ["User: What's the weather?"]
conversation = conversation + ["Bot: I'll check that for you."]

# Get the last exchange
last_exchange = conversation[-2:]  # Last user message and bot response
print("Last exchange:")
for message in last_exchange:
    print(f"  {message}")

# Prepare context for AI (like preparing a prompt)
context_window = 3  # How many previous messages to include
context = conversation[-context_window:] if len(conversation) >= context_window else conversation
print(f"\nContext for next response ({len(context)} messages):")
for msg in context:
    print(f"  {msg}")

# This is exactly how AI agents maintain conversation context!
