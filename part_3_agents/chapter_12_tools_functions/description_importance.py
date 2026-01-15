# From: Zero to AI Agent, Chapter 12, Section 12.2
# File: description_importance.py

from langchain_core.tools import Tool

def same_function(text: str) -> str:
    """This function does text analysis."""
    words = text.split()
    return f"Word count: {len(words)}"

# Same function, different descriptions
vague_tool = Tool(
    name="Analyzer",
    func=same_function,
    description="Analyzes text"  # Too vague!
)

clear_tool = Tool(
    name="WordCounter",
    func=same_function,
    description="Counts the number of words in text. Use when someone asks for word count, length, or size of text."
)

# The LLM will reliably use clear_tool for "How many words are in this?"
# But might not use vague_tool for the same question!
