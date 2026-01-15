# advanced_print.py
# From: Zero to AI Agent, Chapter 2, Section 2.6
# Mastering the print() function

# Multiple items
name = "Alice"
age = 30
print("Name:", name, "Age:", age)  # Automatic spaces between items

# Custom separator
print("apple", "banana", "orange", sep=" | ")  # Custom separator
print("2024", "03", "15", sep="-")  # Date format

# Custom end character (default is newline)
print("Loading", end="")
print(".", end="")
print(".", end="")
print(".", end="")
print(" Done!")  # Finally add newline

# Special characters
print("\n=== Special Characters ===")
print("Line 1\nLine 2\nLine 3")  # Newlines
print("Column1\tColumn2\tColumn3")  # Tabs
print("She said, \"Hello!\"")  # Quotes
print("50% complete")  # Percent sign
print("Unicode: ♥ ★ ☺ ♪")  # Unicode symbols
