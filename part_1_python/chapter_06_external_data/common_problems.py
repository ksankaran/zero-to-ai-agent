# From: Zero to AI Agent, Chapter 6, Section 6.1
# File: common_problems.py

import os
import io

print("🚨 Common File Problems and Solutions 🚨\n")

# Problem 1: File doesn't exist
print("1. Trying to read non-existent file:")
try:
    with open("i_dont_exist.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("   ❌ File not found!")
    print("   ✅ Solution: Check if file exists first\n")

# Solution: Check first
filename = "safe_read.txt"
if os.path.exists(filename):
    with open(filename, "r") as f:
        content = f.read()
else:
    print(f"   File {filename} doesn't exist, creating it...")
    with open(filename, "w") as f:
        f.write("Default content")

# Problem 2: Forgetting to close files
print("\n2. Forgetting to close files:")
files_opened = []
for i in range(3):
    f = open(f"test_{i}.txt", "w")
    f.write("Oops, forgot to close!")
    files_opened.append(f)
    # Forgot f.close()!

print(f"   ⚠️  {len(files_opened)} files still open!")
print("   ✅ Solution: Use 'with' statement")

# Clean up
for f in files_opened:
    f.close()
    os.remove(f.name)  # Clean up test files

# Problem 3: Writing to a file opened for reading
print("\n3. Writing to read-only file:")
with open("readonly_test.txt", "w") as f:
    f.write("Initial content")

try:
    with open("readonly_test.txt", "r") as f:  # Opened for reading
        f.write("Try to write")  # This won't work!
except io.UnsupportedOperation:
    print("   ❌ Can't write to file opened in read mode!")
    print("   ✅ Solution: Use 'r+' or 'w' or 'a' mode")

# Problem 4: Overwriting important data
print("\n4. Accidentally overwriting files:")
with open("important_data.txt", "w") as f:
    f.write("Critical information!")

print("   File has important data...")
# Oops, 'w' mode overwrites!
with open("important_data.txt", "w") as f:  
    f.write("Oops")
    
with open("important_data.txt", "r") as f:
    print(f"   ❌ Data now: '{f.read()}' - Original lost!")
    print("   ✅ Solution: Use 'a' to append, or backup first")

# Problem 5: Platform-specific line endings
print("\n5. Line ending issues:")
with open("line_endings.txt", "w") as f:
    f.write("Line 1\n")  # \n works everywhere in Python
    f.write("Line 2\r\n")  # Windows style (avoid!)
    f.write("Line 3")

with open("line_endings.txt", "r") as f:
    lines = f.readlines()
    print(f"   Python handles line endings automatically!")
    for i, line in enumerate(lines, 1):
        print(f"   Line {i}: {repr(line)}")  # repr shows \n characters

# Cleanup
for filename in ["safe_read.txt", "readonly_test.txt", "important_data.txt", "line_endings.txt"]:
    if os.path.exists(filename):
        os.remove(filename)
