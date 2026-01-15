# From: Zero to AI Agent, Chapter 5, Section 5.7
# File: utils_text_tools.py

# file: utils/text_tools.py
"""Text processing utilities"""

def clean_text(text):
    """Remove extra whitespace and lowercase"""
    return ' '.join(text.split()).lower()

def word_count(text):
    """Count words in text"""
    return len(text.split())

def reverse_string(text):
    """Reverse a string"""
    return text[::-1]