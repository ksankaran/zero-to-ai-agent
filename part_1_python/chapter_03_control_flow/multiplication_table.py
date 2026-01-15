# From: Zero to AI Agent, Chapter 3, Section 3.4
# multiplication_table.py

size = int(input("Enter table size (e.g., 5 for 5x5): "))

print("\n   ", end="")  # Print header row
for i in range(1, size + 1):
    print(f"{i:4}", end="")  # :4 means use 4 spaces for alignment
print()  # New line

print("   " + "-" * (size * 4))  # Separator line

for row in range(1, size + 1):
    print(f"{row:2}|", end="")  # Row label
    for col in range(1, size + 1):
        result = row * col
        print(f"{result:4}", end="")
    print()  # New line after each row
