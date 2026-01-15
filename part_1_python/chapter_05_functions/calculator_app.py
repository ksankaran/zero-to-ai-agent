# From: Zero to AI Agent, Chapter 5, Section 5.2
# File: calculator_app.py

def calculator(num1, num2, operation="add", show_steps=False):
    """
    A flexible calculator function
    Operations: add, subtract, multiply, divide
    """
    if show_steps:
        print(f"Calculating: {num1} {operation} {num2}")
    
    if operation == "add" or operation == "+":
        result = num1 + num2
        symbol = "+"
    elif operation == "subtract" or operation == "-":
        result = num1 - num2
        symbol = "-"
    elif operation == "multiply" or operation == "*":
        result = num1 * num2
        symbol = "×"
    elif operation == "divide" or operation == "/":
        if num2 == 0:
            print("Error: Cannot divide by zero!")
            return None
        result = num1 / num2
        symbol = "÷"
    else:
        print(f"Unknown operation: {operation}")
        return None
    
    if show_steps:
        print(f"Formula: {num1} {symbol} {num2} = {result}")
    else:
        print(f"Result: {result}")
    
    return result

# Use our calculator in different ways
calculator(10, 5)                              # Default: addition
calculator(10, 5, "multiply")                  # Multiplication
calculator(10, 5, operation="divide")          # Using keyword
calculator(10, 5, "-", show_steps=True)       # With steps
calculator(10, 0, "divide")                    # Error handling
