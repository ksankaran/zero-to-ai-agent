# From: Zero to AI Agent, Chapter 5, Section 5.3
# File: simple_calculator.py
# Demonstrates functions with parameters and return values

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return None  # Can't divide by zero
    return a / b

def get_number(prompt):
    """Get a number from user"""
    return float(input(prompt))

def get_operation():
    """Get the operation from user"""
    operations = ['+', '-', '*', '/']
    while True:
        op = input("Enter operation (+, -, *, /): ")
        if op in operations:
            return op
        print("Invalid operation! Try again.")

def calculate(num1, num2, operation):
    """Perform the calculation based on operation"""
    if operation == '+':
        return add(num1, num2)
    elif operation == '-':
        return subtract(num1, num2)
    elif operation == '*':
        return multiply(num1, num2)
    elif operation == '/':
        return divide(num1, num2)

def run_calculator():
    """Main calculator function"""
    print("\n" + "=" * 30)
    print("SIMPLE CALCULATOR")
    print("=" * 30)

    # Get inputs using our functions
    num1 = get_number("Enter first number: ")
    operation = get_operation()
    num2 = get_number("Enter second number: ")

    # Calculate using our function
    result = calculate(num1, num2, operation)

    # Display result
    if result is None:
        print("Error: Cannot divide by zero!")
    else:
        print(f"\n{num1} {operation} {num2} = {result}")

    # Return the result so it can be used elsewhere
    return result

# Run it!
final_result = run_calculator()
print(f"\nThe result was stored as: {final_result}")
