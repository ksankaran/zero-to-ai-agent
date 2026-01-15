# From: Zero to AI Agent, Chapter 4, Section 4.7
# nested_comprehensions.py - Nested loops in comprehensions

# The loop way
pairs_loop = []
for x in [1, 2, 3]:
    for y in ['a', 'b']:
        pairs_loop.append((x, y))
print("Pairs (loop):", pairs_loop)

# The comprehension way
pairs_comp = [(x, y) for x in [1, 2, 3] for y in ['a', 'b']]
print("Pairs (comprehension):", pairs_comp)

# Both give: [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b'), (3, 'a'), (3, 'b')]

# Practical example: Multiplication table
table = [i * j for i in range(1, 4) for j in range(1, 4)]
print("Multiplication:", table)  # [1, 2, 3, 2, 4, 6, 3, 6, 9]

# With better formatting
table_formatted = [(i, j, i*j) for i in range(1, 4) for j in range(1, 4)]
print("\nMultiplication table:")
for i, j, result in table_formatted:
    print(f"{i} × {j} = {result}")
