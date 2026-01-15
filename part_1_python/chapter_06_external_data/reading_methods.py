# From: Zero to AI Agent, Chapter 6, Section 6.1
# File: reading_methods.py

# First, let's create a file with multiple lines
with open("reading_demo.txt", "w") as file:
    file.write("Line 1: Hello!\n")
    file.write("Line 2: How are you?\n")
    file.write("Line 3: Python is amazing!\n")
    file.write("Line 4: Files are fun!\n")
    file.write("Line 5: Keep learning!")

print("Created demo file with 5 lines\n")

# Method 1: read() - Gets everything as one string
print("=== Using read() ===")
with open("reading_demo.txt", "r") as file:
    all_content = file.read()
    print("Everything at once:")
    print(all_content)
    print()

# Method 2: readline() - Gets one line at a time
print("=== Using readline() ===")
with open("reading_demo.txt", "r") as file:
    first_line = file.readline()
    second_line = file.readline()
    print(f"First line: {first_line}", end='')  # Lines already have \n
    print(f"Second line: {second_line}", end='')
    print()

# Method 3: readlines() - Gets all lines as a list
print("=== Using readlines() ===")
with open("reading_demo.txt", "r") as file:
    all_lines = file.readlines()
    print(f"Got {len(all_lines)} lines as a list:")
    for i, line in enumerate(all_lines, 1):
        print(f"  Line {i}: {line}", end='')
    print()

# Method 4: Iteration (most Pythonic for line-by-line)
print("=== Using iteration (best for large files) ===")
with open("reading_demo.txt", "r") as file:
    for line_num, line in enumerate(file, 1):
        print(f"Processing line {line_num}: {line.strip()}")
