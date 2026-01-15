# From: Zero to AI Agent, Chapter 4, Section 4.2
# list_methods_adding.py - Methods for adding items to lists

# Starting with a simple list
topics = ["Python", "Lists", "Loops"]
print("Starting topics:", topics)

# append() - Adds ONE item to the end
topics.append("Functions")
print("After append('Functions'):", topics)

# Be careful - append adds the whole item as ONE element
topics.append(["AI", "ML"])  # This adds the entire list as one item!
print("After appending a list:", topics)
# Notice the nested list: ['Python', 'Lists', 'Loops', 'Functions', ['AI', 'ML']]

# Remove the nested list to clean up
topics.pop()  # Remove last item

# extend() - Adds EACH item from another list
more_topics = ["Machine Learning", "Neural Networks"]
topics.extend(more_topics)
print("After extend:", topics)

# The difference is clear
list_a = [1, 2, 3]
list_b = [4, 5]

# Using append
test_append = list_a.copy()
test_append.append(list_b)
print("\nAppend result:", test_append)  # [1, 2, 3, [4, 5]]

# Using extend
test_extend = list_a.copy()
test_extend.extend(list_b)
print("Extend result:", test_extend)  # [1, 2, 3, 4, 5]

# insert() - Adds an item at a SPECIFIC position
topics = ["Python", "Lists", "Functions", "Classes"]
topics.insert(0, "Introduction")  # Insert at the beginning
print("\nAfter insert at position 0:", topics)

topics.insert(3, "Control Flow")  # Insert at position 3
print("After insert at position 3:", topics)

# Real-world example: Managing a conversation history
chat_history = []
chat_history.append("User: Hello!")
chat_history.append("Bot: Hi there!")
chat_history.insert(0, "System: Conversation started")  # Add system message at beginning
print("\nChat history:")
for message in chat_history:
    print(f"  {message}")
