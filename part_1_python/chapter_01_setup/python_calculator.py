# python_calculator.py
# From: Zero to AI Agent, Chapter 1, Section 1.5

print("🧮 PYTHON CALCULATOR")
print("-" * 20)

# Get user input
first_number = float(input("Enter first number: "))
second_number = float(input("Enter second number: "))

# Perform calculations
sum_result = first_number + second_number
difference = first_number - second_number
product = first_number * second_number

# Avoid division by zero
if second_number != 0:
    quotient = first_number / second_number
else:
    quotient = "Cannot divide by zero!"

# Display results
print("\n📊 RESULTS:")
print("-" * 20)
print(f"{first_number} + {second_number} = {sum_result}")
print(f"{first_number} - {second_number} = {difference}")
print(f"{first_number} × {second_number} = {product}")
print(f"{first_number} ÷ {second_number} = {quotient}")

# Fun with powers
print(f"{first_number} ^ 2 = {first_number ** 2}")
print(f"{second_number} ^ 2 = {second_number ** 2}")