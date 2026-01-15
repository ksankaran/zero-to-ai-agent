# From: Zero to AI Agent, Chapter 4, Section 4.6
# when_to_use_lists.py - When to choose lists for your data

# 1. ORDER MATTERS and items might change
timeline_events = [
    "User logged in",
    "Viewed product",
    "Added to cart",
    "Completed purchase"
]
# The sequence of events is crucial!

# 2. You need to access items by position
temperatures = [22, 24, 23, 25, 21, 26, 22]
monday_temp = temperatures[0]  # First day
friday_temp = temperatures[4]  # Fifth day

# 3. You'll be adding/removing items frequently
task_queue = []
task_queue.append("Process payment")
task_queue.append("Send email")
current_task = task_queue.pop(0)  # Process first task

# 4. Duplicates are allowed and meaningful
dice_rolls = [6, 3, 6, 2, 6, 1, 4, 6]  # Multiple 6s are valid

# 5. You need to sort or reverse
scores = [85, 92, 78, 95, 88]
scores.sort()  # In-place sorting

# Real-world LIST examples in AI:

# Conversation history (order matters, can grow)
chat_messages = [
    "User: Hello",
    "Bot: Hi there!",
    "User: How are you?"
]
chat_messages.append("Bot: I'm doing great!")

# Training data batches (need specific order)
training_batches = [
    [1, 2, 3, 4],  # Batch 1
    [5, 6, 7, 8],  # Batch 2
    [9, 10, 11, 12]  # Batch 3
]

# Sequential predictions
predictions = []
for i in range(5):
    predictions.append(f"Prediction {i}")

print("List examples:")
print(f"Timeline has {len(timeline_events)} events")
print(f"Task queue: {task_queue}")
print(f"Chat messages: {len(chat_messages)} messages")
