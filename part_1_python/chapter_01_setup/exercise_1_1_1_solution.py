# From: Zero to AI Agent, Chapter 1, Section 1.1
# Exercise 1 1.1: The Calculator
# Solution

"""
Simple Calculator
This program asks for two numbers and adds them together.
"""

# Step 1: Ask for the first number
# input() returns text, so we convert it to a number with float()
first_number = float(input("Enter the first number: "))

# Step 2: Ask for the second number
second_number = float(input("Enter the second number: "))

# Step 3: Add them together
result = first_number + second_number

# Step 4: Display the result
print(f"{first_number} + {second_number} = {result}")

# Bonus: You could also show other operations!
# print(f"{first_number} - {second_number} = {first_number - second_number}")
# print(f"{first_number} × {second_number} = {first_number * second_number}")
# print(f"{first_number} ÷ {second_number} = {first_number / second_number}")
