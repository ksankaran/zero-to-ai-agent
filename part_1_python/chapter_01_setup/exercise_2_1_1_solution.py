# From: Zero to AI Agent, Chapter 1, Section 1.1
# Exercise 2 1.1: The Personal Greeter
# Solution

"""
Personal Greeter
This program asks for your name and age, then greets you personally.
"""

# Step 1: Ask for the user's name
name = input("What is your name? ")

# Step 2: Ask for the user's age
age = input("How old are you? ")

# Step 3: Print a personalized message
print(f"Hello {name}, you are {age} years old!")

# Bonus: Calculate birth year (approximately)
# We need to convert age to a number for math
import datetime
current_year = datetime.datetime.now().year
birth_year = current_year - int(age)
print(f"That means you were born around {birth_year}!")
