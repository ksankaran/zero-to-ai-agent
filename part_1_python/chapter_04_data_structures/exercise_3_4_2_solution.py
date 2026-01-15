# From: Zero to AI Agent, Chapter 4, Section 4.2
# Exercise 3: Message Queue

# 1. Initialize queue with max size
queue = []
max_size = 5

# 2. Process messages
messages = ["msg1", "msg2", "msg3", "msg4", "msg5", "msg6", "msg7"]
print(f"Processing {len(messages)} messages...")

for msg in messages:
    if len(queue) >= max_size:
        # Remove oldest message
        removed = queue.pop(0)
        print(f"Queue full, removed: {removed}")
    
    queue.append(msg)
    print(f"Added {msg}, Queue: {queue}")

# 4. Show final queue
print(f"Final queue: {queue}")

# 5. Search for message containing "5"
for i, msg in enumerate(queue):
    if "5" in msg:
        print(f"Found '5' in {msg} at position {i}")
        break

# 6. Count "msg" occurrences
msg_count = sum(1 for msg in queue if "msg" in msg)
print(f"Messages containing 'msg': {msg_count}")
