# From: Zero to AI Agent, Chapter 4, Section 4.1
# list_indexing.py - Accessing list elements with indexing

# Let's create a list of AI terms we'll be using later
ai_terms = ["neural", "network", "training", "model", "agent", "prompt"]

# Accessing items by their index (position)
first_term = ai_terms[0]   # Gets "neural" (index 0)
third_term = ai_terms[2]   # Gets "training" (index 2)

print(f"First term: {first_term}")
print(f"Third term: {third_term}")

# You can also modify items using their index
ai_terms[1] = "NETWORK"    # Changes "network" to "NETWORK"
print("After modification:", ai_terms)

# What happens if we try to access an index that doesn't exist?
# Uncomment the next line to see the error:
# bad_access = ai_terms[10]  # IndexError: list index out of range
