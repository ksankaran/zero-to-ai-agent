# From: Zero to AI Agent, Chapter 4, Section 4.2
# common_patterns.py - Common list patterns for AI applications

# Pattern 1: Building a list conditionally
responses = ["good", "bad", "excellent", "poor", "great", "terrible", "okay"]
positive = []
for response in responses:
    if response in ["good", "excellent", "great"]:
        positive.append(response)
print(f"Positive responses: {positive}")

# Pattern 2: Removing duplicates while preserving order
messages = ["hello", "world", "hello", "python", "world", "ai"]
seen = []
unique_messages = []
for msg in messages:
    if msg not in seen:
        seen.append(msg)
        unique_messages.append(msg)
print(f"Unique messages: {unique_messages}")

# Pattern 3: Batch processing
data = list(range(1, 16))  # 1 to 15
batch_size = 5
print("Processing in batches:")
for i in range(0, len(data), batch_size):
    batch = data[i:i+batch_size]
    print(f"  Processing batch: {batch}")

# Pattern 4: Maintaining a fixed-size history (sliding window)
history = []
max_history = 3

new_items = ["event1", "event2", "event3", "event4", "event5"]
print("Building history with sliding window:")
for item in new_items:
    history.append(item)
    if len(history) > max_history:
        history.pop(0)  # Remove oldest
    print(f"  Current history: {history}")

# Pattern 5: Working with nested lists
# Student scores: [name, [quiz1, quiz2, quiz3]]
students = [
    ["Alice", [85, 90, 92]],
    ["Bob", [78, 82, 88]],
    ["Charlie", [92, 95, 89]]
]

print("\nStudent Score Analysis:")
for student in students:
    name = student[0]
    scores = student[1]
    average = sum(scores) / len(scores)
    highest = max(scores)
    print(f"  {name}: Average = {average:.1f}, Highest = {highest}")
