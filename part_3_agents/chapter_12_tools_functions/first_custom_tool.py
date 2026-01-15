# From: Zero to AI Agent, Chapter 12, Section 12.2
# File: first_custom_tool.py

from langchain_core.tools import Tool

# Step 1: Create a regular Python function
def greet(name: str) -> str:
    """Generate a friendly greeting."""
    return f"Hello {name}! Welcome to the world of custom tools!"

# Step 2: Wrap it as a LangChain tool
greeting_tool = Tool(
    name="Greeter",  # What the LLM will call this
    func=greet,      # The function to run
    description="Use this to greet someone by name"  # When to use it
)

# Test it directly
result = greeting_tool.func("Alice")
print(result)  # "Hello Alice! Welcome to the world of custom tools!"
