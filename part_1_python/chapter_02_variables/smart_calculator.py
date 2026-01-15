# smart_calculator.py
# From: Zero to AI Agent, Chapter 2, Section 2.2
# A simple calculator demonstrating arithmetic operations

print("=" * 40)
print("SIMPLE CALCULATOR")
print("=" * 40)

# Get two numbers from the user
first_number = float(input("Enter first number: "))
second_number = float(input("Enter second number: "))

# Perform all arithmetic operations
addition = first_number + second_number
subtraction = first_number - second_number
multiplication = first_number * second_number
division = first_number / second_number
power = first_number ** second_number

# Display results
print("")
print("=" * 40)
print("RESULTS")
print("=" * 40)
print(f"{first_number} + {second_number} = {addition}")
print(f"{first_number} - {second_number} = {subtraction}")
print(f"{first_number} * {second_number} = {multiplication}")
print(f"{first_number} / {second_number} = {division}")
print(f"{first_number} ** {second_number} = {power}")
print("=" * 40)
