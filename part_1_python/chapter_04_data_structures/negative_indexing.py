# From: Zero to AI Agent, Chapter 4, Section 4.1
# negative_indexing.py - Counting from the end with negative indices

# Using the same AI terms list
ai_terms = ["neural", "network", "training", "model", "agent", "prompt"]

# Negative indexing starts from the end
last_term = ai_terms[-1]       # Gets "prompt"
second_to_last = ai_terms[-2]  # Gets "agent"
third_from_end = ai_terms[-3]  # Gets "model"

print(f"Last term: {last_term}")
print(f"Second to last: {second_to_last}")
print(f"Third from end: {third_from_end}")

# This is incredibly useful! Imagine you're building a chatbot
chat_history = ["Hello", "How are you?", "I'm fine", "What's the weather?", "It's sunny"]
last_message = chat_history[-1]  # Always gets the most recent message
print(f"Most recent message: {last_message}")
