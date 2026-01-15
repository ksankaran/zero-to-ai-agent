# variable_labels.py
# From: Zero to AI Agent, Chapter 2, Section 2.1

# Variables are like labels, not boxes
original_name = "Alice"
also_alice = original_name  # This doesn't copy Alice, it adds another label

print("Original:", original_name)
print("Also:", also_alice)

# Now let's move the original_name label to something else
original_name = "Bob"

print("\nAfter change:")
print("Original:", original_name)  # Now Bob
print("Also:", also_alice)         # Still Alice!
