# From: Zero to AI Agent, Chapter 5, Section 5.6
# File: collections_module_demo.py

from collections import Counter, defaultdict, deque

# Counter - count things easily
text = "hello world"
letter_counts = Counter(text)
print(f"Letter counts: {letter_counts}")
print(f"Most common: {letter_counts.most_common(3)}")

# defaultdict - dictionaries with default values
word_list = defaultdict(list)  # Default value is empty list
word_list["fruits"].append("apple")
word_list["fruits"].append("banana")
word_list["vegetables"].append("carrot")
print(f"Word list: {dict(word_list)}")

# deque - efficient list for adding/removing from ends
queue = deque([1, 2, 3])
queue.append(4)      # Add to right
queue.appendleft(0)  # Add to left
print(f"Queue: {list(queue)}")
first = queue.popleft()  # Remove from left
print(f"Removed {first}, queue now: {list(queue)}")