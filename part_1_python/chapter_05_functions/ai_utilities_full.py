# From: Zero to AI Agent, Chapter 5, Section 5.7
# File: ai_utilities_full.py

# file: ai_utils.py
"""
AI Utilities Module
Helpful functions for AI and text processing projects
"""

import re
import json
import time
from datetime import datetime

# Constants
MAX_TOKEN_LENGTH = 4000  # Typical AI model limit
DEFAULT_TEMPERATURE = 0.7

def clean_for_ai(text):
    """
    Clean text for AI processing
    - Remove extra whitespace
    - Fix common encoding issues
    - Limit length
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Fix common issues
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")
    
    # Remove control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char == '\n')
    
    # Truncate if too long (leave room for prompt)
    if len(text) > MAX_TOKEN_LENGTH:
        text = text[:MAX_TOKEN_LENGTH] + "..."
    
    return text

def chunk_text(text, chunk_size=1000, overlap=100):
    """
    Split text into overlapping chunks for processing
    Useful when text is too long for AI models
    """
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # Overlap for context
    
    return chunks

def extract_code_blocks(text):
    """Extract code blocks from markdown text"""
    pattern = r'```(?:\w+)?\n(.*?)```'
    code_blocks = re.findall(pattern, text, re.DOTALL)
    return code_blocks

def format_prompt(instruction, context="", examples=None):
    """
    Format a prompt for AI models
    
    Args:
        instruction: Main instruction for the AI
        context: Optional context information
        examples: Optional list of example inputs/outputs
    """
    prompt_parts = []
    
    if context:
        prompt_parts.append(f"Context: {context}\n")
    
    if examples:
        prompt_parts.append("Examples:")
        for i, example in enumerate(examples, 1):
            prompt_parts.append(f"  Example {i}:")
            prompt_parts.append(f"    Input: {example.get('input', '')}")
            prompt_parts.append(f"    Output: {example.get('output', '')}")
        prompt_parts.append("")
    
    prompt_parts.append(f"Instruction: {instruction}")
    
    return "\n".join(prompt_parts)

def measure_tokens_approximate(text):
    """
    Approximate token count (rough estimate)
    Actual tokenization is model-specific
    Rule of thumb: ~4 characters per token
    """
    return len(text) // 4

def create_conversation_log(messages, filename=None):
    """Save conversation to JSON file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.json"
    
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "message_count": len(messages),
        "messages": messages
    }
    
    with open(filename, 'w') as f:
        json.dump(log_data, f, indent=2)
    
    return filename

class ResponseTimer:
    """Context manager to time AI responses"""
    
    def __init__(self, label="Response"):
        self.label = label
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, *args):
        self.end_time = time.time()
        elapsed = self.end_time - self.start_time
        print(f"{self.label} took {elapsed:.2f} seconds")
    
    @property
    def elapsed(self):
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time

# Module testing
if __name__ == "__main__":
    print("AI Utils Module Test")
    print("-" * 40)
    
    # Test text cleaning
    messy_text = "  This   is   messy   text   with   spaces  "
    cleaned = clean_for_ai(messy_text)
    print(f"Cleaned: '{cleaned}'")
    
    # Test prompt formatting
    prompt = format_prompt(
        instruction="Translate to Spanish",
        context="Informal conversation",
        examples=[
            {"input": "Hello", "output": "Hola"},
            {"input": "Thank you", "output": "Gracias"}
        ]
    )
    print(f"\nFormatted prompt:\n{prompt}")
    
    # Test timer
    with ResponseTimer("Test operation"):
        time.sleep(1)  # Simulate work
    
    print("\nModule ready for use in AI projects!")