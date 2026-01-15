# From: Zero to AI Agent, Chapter 5, Section 5.3
# File: analyze_text.py

def analyze_text(text):
    """Return multiple statistics about text"""
    word_count = len(text.split())
    char_count = len(text)
    char_no_spaces = len(text.replace(" ", ""))
    
    return word_count, char_count, char_no_spaces

# Analyze some text
text = "Python functions are amazing and powerful"
words, chars, chars_no_space = analyze_text(text)

print(f"Words: {words}")
print(f"Characters (with spaces): {chars}")
print(f"Characters (no spaces): {chars_no_space}")