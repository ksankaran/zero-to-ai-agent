# From: Zero to AI Agent, Chapter 5, Section 5.1
# File: defining_vs_calling.py
# Topic: The difference between defining and calling functions

# This DEFINES a function (creates the recipe)
def sing_happy_birthday():
    print("Happy birthday to you!")
    print("Happy birthday to you!")
    print("Happy birthday dear friend!")
    print("Happy birthday to you!")

# At this point, nothing has been printed yet!
# The function exists, but hasn't been used.

# This CALLS the function (follows the recipe)
sing_happy_birthday()  # NOW it prints!

# We can call it multiple times
sing_happy_birthday()  # Prints again
sing_happy_birthday()  # And again!
