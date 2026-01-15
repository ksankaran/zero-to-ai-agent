# creating_strings.py
# From: Zero to AI Agent, Chapter 2, Section 2.3
# Three ways to create strings in Python

# Method 1: Single quotes
name = 'Alice'
mood = 'happy'
print("Single quotes:", name, "is", mood)

# Method 2: Double quotes
greeting = "Hello, World!"
company = "Bob's Burgers"  # Can use apostrophes inside double quotes!
print("Double quotes:", greeting)
print("Apostrophe inside:", company)

# Method 3: Triple quotes (for multiple lines)
long_text = """This is a longer piece of text.
It can span multiple lines.
Perfect for paragraphs or documentation!"""
print("\nTriple quotes:")
print(long_text)

# Triple quotes with single quotes work too
poem = '''Roses are red,
Violets are blue,
Python is awesome,
And so are you!'''
print("\nA poem for you:")
print(poem)
