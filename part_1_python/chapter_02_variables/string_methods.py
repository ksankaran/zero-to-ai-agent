# string_methods.py
# From: Zero to AI Agent, Chapter 2, Section 2.3
# Essential string methods you'll use constantly

text = "  Python Programming is Fun!  "

# Case transformations
print("Original:", f"'{text}'")
print("Upper:", text.upper())
print("Lower:", text.lower())
print("Title Case:", text.title())
print("Capitalize:", text.capitalize())
print("Swap Case:", text.swapcase())

# Cleaning up strings
print("\n--- Cleaning ---")
print("Strip spaces:", f"'{text.strip()}'")
print("Left strip:", f"'{text.lstrip()}'")
print("Right strip:", f"'{text.rstrip()}'")

# Finding and replacing
print("\n--- Find & Replace ---")
sentence = "Python is awesome. Python is powerful."
print("Original:", sentence)
print("Replace:", sentence.replace("Python", "JavaScript"))
print("Replace first only:", sentence.replace("Python", "JavaScript", 1))
print("Find 'awesome':", sentence.find("awesome"))  # Returns index
print("Count 'Python':", sentence.count("Python"))

# Checking string properties
print("\n--- String Checks ---")
print("'hello'.isalpha():", "hello".isalpha())  # All letters?
print("'123'.isdigit():", "123".isdigit())      # All digits?
print("'Hello123'.isalnum():", "Hello123".isalnum())  # Letters/digits only?
print("'  '.isspace():", "  ".isspace())         # All whitespace?
print("'Title Case'.istitle():", "Title Case".istitle())  # Title case?

# Splitting and joining
print("\n--- Split & Join ---")
data = "apple,banana,orange,grape"
fruits = data.split(",")
print("Split by comma:", fruits)
rejoined = " | ".join(fruits)
print("Joined with pipe:", rejoined)

# Multi-line splitting
address = """123 Main St
New York, NY
10001"""
lines = address.splitlines()
print("\nAddress lines:", lines)
