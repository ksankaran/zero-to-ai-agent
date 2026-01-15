# From: Zero to AI Agent, Chapter 6, Section 6.1
# File: first_file.py

# Writing to a file
file = open("my_first_file.txt", "w")  # "w" means "write mode"
file.write("Hello, File System!")
file.write("\nThis is my first file operation!")
file.close()  # IMPORTANT: Always close your files!

print("File created! Check your folder - you'll see my_first_file.txt")

# Reading from a file
file = open("my_first_file.txt", "r")  # "r" means "read mode"
content = file.read()
file.close()

print("I read from the file:")
print(content)
