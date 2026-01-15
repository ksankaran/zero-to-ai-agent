# From: Zero to AI Agent, Chapter 4, Section 4.5
# set_performance.py - Why sets are incredibly fast

import time

# Create large collections
large_list = list(range(1000000))
large_set = set(range(1000000))

# Test membership with list (slow for large lists)
start = time.time()
result = 999999 in large_list  # Has to check each element until found
list_time = time.time() - start

# Test membership with set (always fast)
start = time.time()
result = 999999 in large_set  # Direct lookup
set_time = time.time() - start

print(f"List lookup time: {list_time:.6f} seconds")
print(f"Set lookup time: {set_time:.6f} seconds")
print(f"Set is {list_time/set_time:.0f}x faster!")

# Practical example: Checking many items
words_to_check = ["python", "programming", "ai", "machine", "learning"] * 1000
valid_words = {"python", "programming", "ai", "computer", "science", "data"}

# Using set for validation (fast)
start = time.time()
valid_count = sum(1 for word in words_to_check if word in valid_words)
print(f"\nValidation with set: {time.time() - start:.4f} seconds")
print(f"Found {valid_count} valid words")
