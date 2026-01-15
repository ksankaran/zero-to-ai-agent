# From: Zero to AI Agent, Chapter 4, Section 4.5
# set_creation.py - Creating sets in Python

# Creating sets - notice just values, no key:value pairs
fruits = {"apple", "banana", "orange", "grape"}
print(f"Fruits set: {fruits}")
print(f"Type: {type(fruits)}")

# Sets automatically remove duplicates!
numbers = {1, 2, 3, 2, 1, 4, 3, 5}  # Duplicates: 1, 2, 3
print(f"Numbers set: {numbers}")  # Only unique values remain

# Creating from a list (removes duplicates)
temperatures = [22, 24, 22, 23, 24, 25, 23, 22]
unique_temps = set(temperatures)
print(f"Original list: {temperatures}")
print(f"Unique temperatures: {unique_temps}")

# Empty set - CAREFUL with this one!
# wrong_way = {}  # This creates an empty DICTIONARY, not a set!
right_way = set()  # This creates an empty set
also_right = {1, 2, 3}
also_right.clear()  # Now it's empty
print(f"Empty set: {right_way}")
print(f"Type of {{}}: {type({})}")  # It's a dict!
print(f"Type of set(): {type(set())}")  # It's a set!

# Creating from a string (gets unique characters)
word = "programming"
unique_letters = set(word)
print(f"Unique letters in '{word}': {unique_letters}")

# Creating from range
evens = set(range(0, 10, 2))
print(f"Even numbers: {evens}")
