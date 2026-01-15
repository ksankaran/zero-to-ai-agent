# From: Zero to AI Agent, Chapter 4, Section 4.7
# performance_test.py - Testing if comprehensions are faster than loops

import time

# Large dataset
n = 1000000
data = list(range(n))

# Using a loop
start = time.time()
squares_loop = []
for x in data:
    squares_loop.append(x ** 2)
loop_time = time.time() - start

# Using comprehension
start = time.time()
squares_comp = [x ** 2 for x in data]
comp_time = time.time() - start

print(f"Loop time: {loop_time:.3f} seconds")
print(f"Comprehension time: {comp_time:.3f} seconds")
print(f"Comprehension is {loop_time/comp_time:.1f}x faster!")

# Comprehensions are usually faster because:
# 1. They're optimized at the C level
# 2. Less Python bytecode to interpret
# 3. No repeated append() method calls
