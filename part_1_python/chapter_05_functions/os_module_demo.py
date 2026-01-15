# From: Zero to AI Agent, Chapter 5, Section 5.6
# File: os_module_demo.py

import os

# Get current working directory
current_dir = os.getcwd()
print(f"Current directory: {current_dir}")

# List files in a directory
files = os.listdir(".")  # "." means current directory
print(f"Files here: {files[:5]}...")  # Show first 5

# Check if a file exists
if os.path.exists("my_file.txt"):
    print("File exists!")
else:
    print("File doesn't exist")

# Create a directory (folder)
if not os.path.exists("my_new_folder"):
    os.makedirs("my_new_folder")
    print("Created new folder!")

# Get environment variables (useful for API keys later!)
# Example: getting the HOME directory
home = os.getenv("HOME", "Not found")
print(f"Home directory: {home}")