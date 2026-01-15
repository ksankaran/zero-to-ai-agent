# From: Zero to AI Agent, Chapter 4, Section 4.3
# tuple_creation.py - Creating tuples in Python

# Creating tuples - notice the parentheses!
coordinates = (10, 20)
print(f"Coordinates: {coordinates}")
print(f"Type: {type(coordinates)}")

# Tuple with different data types
person = ("Alice", 25, "Engineer", True)
print(f"Person data: {person}")

# Empty tuple
empty = ()
print(f"Empty tuple: {empty}")

# Here's where it gets interesting - parentheses are often optional!
colors = "red", "green", "blue"  # This is a tuple!
print(f"Colors: {colors}")
print(f"Type: {type(colors)}")

# But sometimes parentheses are required for clarity
# Without parentheses, this would be confusing:
result = (1 + 2, 3 + 4)  # Tuple of (3, 7)
print(f"Result: {result}")

# Single element tuple - this is tricky!
not_a_tuple = (42)  # This is just the number 42 with parentheses
actual_tuple = (42,)  # The comma makes it a tuple!
print(f"not_a_tuple: {not_a_tuple}, type: {type(not_a_tuple)}")
print(f"actual_tuple: {actual_tuple}, type: {type(actual_tuple)}")

# Converting a list to a tuple
my_list = [1, 2, 3, 4, 5]
my_tuple = tuple(my_list)
print(f"List converted to tuple: {my_tuple}")
