# From: Zero to AI Agent, Chapter 6, Section 6.1
# File: file_modes.py

# Mode 'r' - Read (default)
# Can only read, file must exist
reading_file = open("my_first_file.txt", "r")
content = reading_file.read()
reading_file.close()
print("Read mode content:", content)

# Mode 'w' - Write (careful - overwrites!)
# Creates new file or OVERWRITES existing
writing_file = open("new_file.txt", "w")
writing_file.write("This is brand new content!")
writing_file.close()
print("Created new_file.txt")

# Mode 'a' - Append (safe for adding)
# Adds to the end, doesn't overwrite
appending_file = open("new_file.txt", "a")
appending_file.write("\nThis was added later!")
appending_file.close()
print("Added content to new_file.txt")

# Mode 'r+' - Read and Write
# File must exist, can read and write
read_write_file = open("new_file.txt", "r+")
current = read_write_file.read()
read_write_file.write("\nAnd even more content!")
read_write_file.close()
print("Read and added content")
