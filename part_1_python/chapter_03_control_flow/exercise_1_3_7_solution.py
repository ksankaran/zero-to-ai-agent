# From: Zero to AI Agent, Chapter 3, Section 3.7
# Exercise 1: Multiplication Table Generator
# Generate a formatted multiplication table using nested loops

print("=" * 40)
print("MULTIPLICATION TABLE GENERATOR")
print("=" * 40)

# Get table size
size = int(input("Enter table size (e.g., 5 for 5x5): "))

# Print header row
print("\n    ", end="")  # Space for row labels
for col in range(1, size + 1):
    print(f"{col:4}", end="")
print()  # New line

# Print separator
print("    " + "-" * (size * 4))

# Print each row using nested loops
for row in range(1, size + 1):
    print(f"{row:3}|", end="")  # Row label

    for col in range(1, size + 1):
        result = row * col

        # Highlight diagonal where row == col
        if row == col:
            print(f"[{result:2}]", end="")
        else:
            print(f"{result:4}", end="")

    print()  # New line after each row

print("")
print("Note: Numbers in brackets [] are on the diagonal")
print("=" * 40)
