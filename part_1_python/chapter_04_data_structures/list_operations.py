# From: Zero to AI Agent, Chapter 4, Section 4.2
# list_operations.py - Mathematical operations with lists

# Concatenation with +
list_a = [1, 2, 3]
list_b = [4, 5, 6]
combined = list_a + list_b
print(f"{list_a} + {list_b} = {combined}")

# Repetition with *
pattern = [0, 1]
repeated = pattern * 3
print(f"{pattern} * 3 = {repeated}")

# This is great for initialization!
# Creating a game board
row = [0] * 5  # Five zeros
board = []
for i in range(5):
    board.append(row.copy())  # Important: copy each row!
print("Empty board:")
for row in board:
    print(row)

# Membership testing (we saw this earlier)
inventory = ["sword", "shield", "potion", "map"]
has_potion = "potion" in inventory
has_armor = "armor" in inventory
print(f"Has potion? {has_potion}")
print(f"Has armor? {has_armor}")

# Length, min, max, sum (for numeric lists)
numbers = [10, 5, 8, 3, 15, 12]
print(f"Length: {len(numbers)}")
print(f"Minimum: {min(numbers)}")
print(f"Maximum: {max(numbers)}")
print(f"Sum: {sum(numbers)}")
print(f"Average: {sum(numbers) / len(numbers)}")
