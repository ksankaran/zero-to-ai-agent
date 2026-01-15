# From: Zero to AI Agent, Chapter 12, Section 12.6
# File: helpful_error_messages.py

from langchain_core.tools import Tool

def file_tool_with_helpful_errors(command: str) -> str:
    """
    File tool that provides actionable error messages.
    """
    parts = command.split()
    if not parts:
        return """Error: No command provided.
        
How to use this tool:
- 'read <filename>' - Read a file
- 'write <filename> <content>' - Write to a file
- 'list' - List files in current directory
        
Example: 'read document.txt'"""
    
    action = parts[0].lower()
    
    if action == "read":
        if len(parts) < 2:
            return """Error: Filename required for read command.
            
Correct format: 'read <filename>'
Example: 'read report.pdf'
            
Available files: document.txt, data.csv, notes.md"""
        
        filename = parts[1]
        
        # Simulate file not found
        if filename not in ["document.txt", "data.csv", "notes.md"]:
            return f"""Error: File '{filename}' not found.
            
Did you mean one of these?
- document.txt
- data.csv  
- notes.md
            
To see all files, use: 'list'"""
        
        return f"Contents of {filename}: [file contents here]"
    
    elif action == "write":
        if len(parts) < 3:
            return """Error: Write command requires filename and content.
            
Correct format: 'write <filename> <content>'
Example: 'write notes.txt Meeting at 3pm'
            
Note: Content will be written as a single line."""
        
        return f"Successfully wrote to {parts[1]}"
    
    elif action == "list":
        return """Files in current directory:
- document.txt (1.2 KB) - Last modified: 2024-03-15
- data.csv (5.6 KB) - Last modified: 2024-03-14  
- notes.md (850 B) - Last modified: 2024-03-15"""
    
    else:
        return f"""Error: Unknown command '{action}'.
        
Available commands:
- read: Read a file
- write: Write to a file
- list: Show all files
        
Type the command followed by any required parameters.
Example: 'read document.txt'"""

# Test helpful errors
print("HELPFUL ERROR MESSAGES")
print("=" * 50)

tool = Tool(
    name="FileTool",
    func=file_tool_with_helpful_errors,
    description="File operations with helpful errors"
)

test_commands = [
    "",                    # No command
    "read",               # Missing filename
    "read missing.txt",   # File not found
    "write notes.txt",    # Missing content
    "invalid",            # Unknown command
    "read document.txt",  # Success case
]

for cmd in test_commands:
    print(f"\nCommand: '{cmd}'")
    print("-" * 40)
    result = tool.func(cmd)
    print(result)
