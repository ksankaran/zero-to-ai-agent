# From: Zero to AI Agent, Chapter 4, Section 4.6
# performance_comparison.py - Comparing performance of different data structures

import time

# Setup
n = 100000
test_list = list(range(n))
test_set = set(range(n))
test_dict = {}
for i in range(n):
    test_dict[i] = i

# MEMBERSHIP TESTING
search_value = n - 1

# List (slow for large collections)
start = time.time()
result = search_value in test_list
list_time = time.time() - start

# Set (always fast)
start = time.time()
result = search_value in test_set
set_time = time.time() - start

# Dictionary (always fast)
start = time.time()
result = search_value in test_dict
dict_time = time.time() - start

print(f"Membership testing for {n} items:")
print(f"  List: {list_time:.6f} seconds")
print(f"  Set: {set_time:.6f} seconds")
print(f"  Dict: {dict_time:.6f} seconds")

# ADDING ITEMS
# List append (fast)
start = time.time()
test_list.append(n)
print(f"\nAdding one item:")
print(f"  List append: {time.time() - start:.6f} seconds")

# Set add (fast)
start = time.time()
test_set.add(n)
print(f"  Set add: {time.time() - start:.6f} seconds")

# Dictionary assignment (fast)
start = time.time()
test_dict[n] = n
print(f"  Dict assign: {time.time() - start:.6f} seconds")

