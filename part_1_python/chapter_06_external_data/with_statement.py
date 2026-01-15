# From: Zero to AI Agent, Chapter 6, Section 6.1
# File: with_statement.py

# The risky old way (what we've been doing)
file = open("risky.txt", "w")
file.write("This is risky...")
# What if your program crashes here? File never closes!
file.close()

# The safe new way (what professionals do)
with open("safe.txt", "w") as file:
    file.write("This is safe!")
    file.write("\nEven if something goes wrong...")
    # File automatically closes when we leave this indented block!

print("File automatically closed - we're safe!")

# Reading with 'with' statement
with open("safe.txt", "r") as file:
    content = file.read()
    print("Read safely:", content)
# File is already closed here!
