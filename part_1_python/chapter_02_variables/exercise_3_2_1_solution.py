# Exercise 3: Variable Swap Challenge
# Given first_item = "coffee" and second_item = "tea", swap their values
# Hint: You might need a third variable!

# Solution:

# Initial values
first_item = "coffee"
second_item = "tea"

print("Before swap:")
print("first_item =", first_item)
print("second_item =", second_item)

# Method 1: Using a temporary variable (classic approach)
temp = first_item         # Store first_item in temp
first_item = second_item  # Put second_item into first_item
second_item = temp        # Put temp (original first_item) into second_item

print("\nAfter swap (Method 1):")
print("first_item =", first_item)
print("second_item =", second_item)

# Reset for Method 2
first_item = "coffee"
second_item = "tea"

# Method 2: Python's tuple unpacking (the Pythonic way!)
# This is a preview of a more advanced feature
first_item, second_item = second_item, first_item

print("\nAfter swap (Method 2 - Python's special syntax):")
print("first_item =", first_item)
print("second_item =", second_item)

# Reset for Method 3
first_item = "coffee"
second_item = "tea"

# Method 3: Without a temp variable (works for strings)
# This is a clever trick using string concatenation
first_item = first_item + second_item  # "coffeetea"
second_item = first_item[0:6]          # Extract "coffee"
first_item = first_item[6:]            # Extract "tea"

print("\nAfter swap (Method 3 - string trick):")
print("first_item =", first_item)
print("second_item =", second_item)
