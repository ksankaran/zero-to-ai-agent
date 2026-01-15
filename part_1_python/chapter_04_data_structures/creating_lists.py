# From: Zero to AI Agent, Chapter 4, Section 4.1
# creating_lists.py - All the ways to create lists

# Method 1: Direct creation (what we just did)
colors = ["red", "blue", "green", "yellow"]
print("Method 1 - Direct creation:", colors)

# Method 2: Creating from a string
sentence = "Python is amazing"
words = sentence.split()  # Splits the string into a list of words
print("Method 2 - From string:", words)

# Method 3: Using the list() function
numbers_string = "12345"
digits = list(numbers_string)  # Converts each character to a list item
print("Method 3 - Using list():", digits)

# Method 4: Creating with range() - remember this from loops?
counting = list(range(1, 11))  # Numbers 1 through 10
print("Method 4 - Using range():", counting)

# Method 5: Repeating elements
lots_of_zeros = [0] * 5  # Creates [0, 0, 0, 0, 0]
print("Method 5 - Repetition:", lots_of_zeros)
