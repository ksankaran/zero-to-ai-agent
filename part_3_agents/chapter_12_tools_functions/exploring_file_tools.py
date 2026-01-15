# From: Zero to AI Agent, Chapter 12, Section 12.3
# File: exploring_file_tools.py

from langchain_community.tools import (
    WriteFileTool,
    ReadFileTool,
    ListDirectoryTool
)
import tempfile
import os

# Create a temporary directory to work in safely
working_dir = tempfile.mkdtemp(prefix="tools_exploration_")
print(f"Working directory: {working_dir}")
print("=" * 50)

# Initialize file tools with the working directory
write_tool = WriteFileTool(root_dir=working_dir)
read_tool = ReadFileTool(root_dir=working_dir)
list_tool = ListDirectoryTool(root_dir=working_dir)

# Test 1: Write a file
print("\n1. Testing WriteFileTool:")
write_result = write_tool.run({
    "file_path": "test_note.txt",
    "text": "Hello from LangChain tools!\nThis is a test file."
})
print(f"   Result: {write_result}")

# Test 2: List directory contents
print("\n2. Testing ListDirectoryTool:")
list_result = list_tool.run({"dir_path": "."})
print(f"   Contents: {list_result}")

# Test 3: Read the file back
print("\n3. Testing ReadFileTool:")
read_result = read_tool.run({"file_path": "test_note.txt"})
print(f"   File contents: {read_result}")

# Test 4: Create a more complex file
print("\n4. Creating a Python script:")
python_code = '''def greet(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("World"))
'''
write_tool.run({
    "file_path": "hello.py",
    "text": python_code
})
print("   Created hello.py")

# List files again
final_list = list_tool.run({"dir_path": "."})
print(f"\n5. Final directory contents: {final_list}")

# Clean up
print(f"\nFiles created in: {working_dir}")
print("(This is a temporary directory)")
