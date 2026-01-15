# working_with_floats.py
# From: Zero to AI Agent, Chapter 2, Section 2.2
# Floats are numbers with decimal points

# Common floats
price = 19.99
height_in_meters = 1.75
pi = 3.14159
tiny_number = 0.00001

# Even if it looks like a whole number, adding .0 makes it a float
distance = 10.0  # This is a float, not an integer!
age = 25.0      # Also a float

# Scientific notation automatically creates floats
scientific = 1.23e4  # This is 1.23 × 10^4 = 12300.0
print("Scientific notation:", scientific)

# Let's check the types
print("Type of price:", type(price))
print("Type of distance:", type(distance))  # Note: It's a float!
print("Type of 10:", type(10))              # Compare with integer
