# string_concatenation.py
# From: Zero to AI Agent, Chapter 2, Section 2.3
# Different ways to combine strings

# Method 1: Using the + operator
first_name = "John"
last_name = "Doe"
full_name = first_name + " " + last_name
print("Full name:", full_name)

# Method 2: Using f-strings (formatted strings) - MODERN AND PREFERRED!
age = 30
city = "New York"
introduction = f"My name is {full_name}, I'm {age} years old, and I live in {city}."
print(introduction)

# You can do calculations inside f-strings!
items = 3
price = 19.99
message = f"You bought {items} items for a total of ${items * price:.2f}"
print(message)

# Method 3: Using .format() (older but still common)
template = "Hello, {}! Welcome to {}.".format("Alice", "Python Land")
print(template)

# Method 4: Using % formatting (very old style, might see in old code)
old_style = "Name: %s, Age: %d" % ("Bob", 25)
print(old_style)

# Method 5: Using join() for lists of strings
words = ["Python", "is", "really", "awesome"]
sentence = " ".join(words)
print("Joined:", sentence)
