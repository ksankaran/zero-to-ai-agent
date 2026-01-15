# From: Zero to AI Agent, Chapter 6, Section 6.1
# File: file_paths.py

import os

# Relative paths (relative to where your script is)
with open("same_folder.txt", "w") as f:
    f.write("This file is in the same folder as the script")

# Creating a subfolder and file
if not os.path.exists("notes"):
    os.makedirs("notes")

with open("notes/organized.txt", "w") as f:
    f.write("This file is in the 'notes' subfolder")

# Going up a directory (.. means parent directory)
# with open("../file_in_parent.txt", "w") as f:
#     f.write("This would be in the parent directory")

# Absolute paths (full path from root)
home = os.path.expanduser("~")  # Gets your home directory
desktop_path = os.path.join(home, "Desktop", "my_file.txt")
print(f"Full path to desktop: {desktop_path}")

# Getting information about paths
current_dir = os.getcwd()
print(f"Current directory: {current_dir}")

script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Script directory: {script_dir}")

# Listing files in current directory
print("\nFiles in current directory:")
for file in os.listdir("."):
    if os.path.isfile(file):
        size = os.path.getsize(file)
        print(f"  📄 {file} ({size} bytes)")
