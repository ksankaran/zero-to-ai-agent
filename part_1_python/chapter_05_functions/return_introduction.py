# From: Zero to AI Agent, Chapter 5, Section 5.3
# File: return_introduction.py

# A function that returns a value
def add_numbers_good(x, y):
    result = x + y
    return result  # Send the value back!

# Now we can use the result!
total = add_numbers_good(5, 3)
print(f"The total is {total}")

# We can use it in calculations
double_total = total * 2
print(f"Double that is {double_total}")

# We can use it in conditions
if total > 7:
    print("That's bigger than 7!")