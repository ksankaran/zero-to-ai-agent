# From: Zero to AI Agent, Chapter 12, Section 12.2
# File: exercise_3_12_2_solution.py

from langchain_core.tools import Tool
from datetime import datetime

class SimpleFileSystem:
    """Simulated file system."""
    
    def __init__(self):
        self.files = {}
    
    def parse_command(self, command: str) -> str:
        """Parse and execute file commands."""
        try:
            cmd = command.lower().strip()
            
            if cmd.startswith("create "):
                parts = cmd[7:].split(" with ")
                if len(parts) == 2:
                    filename, content = parts[0].strip(), parts[1].strip()
                    if filename in self.files:
                        return f"Error: {filename} already exists"
                    self.files[filename] = {
                        'content': content,
                        'created': datetime.now().isoformat()
                    }
                    return f"Created {filename}"
                return "Error: Use 'create file.txt with content'"
            
            elif cmd.startswith("read "):
                filename = cmd[5:].strip()
                if filename not in self.files:
                    return f"Error: {filename} not found"
                return f"Content: {self.files[filename]['content']}"
            
            elif cmd == "list files" or cmd == "list":
                if not self.files:
                    return "No files"
                return "Files: " + ", ".join(self.files.keys())
            
            elif cmd.startswith("delete "):
                filename = cmd[7:].strip()
                if filename not in self.files:
                    return f"Error: {filename} not found"
                del self.files[filename]
                return f"Deleted {filename}"
            
            elif cmd.startswith("search "):
                term = cmd[7:].strip()
                matches = []
                for name, data in self.files.items():
                    if term in data['content'].lower():
                        matches.append(name)
                return f"Found in: {', '.join(matches)}" if matches else "No matches"
            
            else:
                return "Commands: create, read, list, delete, search"
                
        except Exception as e:
            return f"Error: {str(e)}"

# Create file system instance
fs = SimpleFileSystem()

# Create tool
file_manager = Tool(
    name="FileManager",
    func=fs.parse_command,
    description="Manage files: 'create file.txt with content', 'read file.txt', 'list files', 'delete file.txt', 'search term'"
)

# Test
if __name__ == "__main__":
    print(file_manager.func("create test.txt with Hello World"))
    print(file_manager.func("list files"))
    print(file_manager.func("read test.txt"))
    print(file_manager.func("search Hello"))
    print(file_manager.func("delete test.txt"))
