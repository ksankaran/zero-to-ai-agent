# From: Zero to AI Agent, Chapter 12, Section 12.2
# File: calculator_tool.py

from langchain_core.tools import Tool
import re

def safe_calculator(expression: str) -> str:
    """
    A calculator that safely evaluates mathematical expressions.
    Returns the result or an error message.
    """
    try:
        # Clean the expression - remove spaces and commas
        expression = expression.replace(" ", "").replace(",", "")
        
        # Only allow numbers and basic math operators
        if not re.match(r'^[0-9+\-*/().\s]+$', expression):
            return "Error: Only numbers and +, -, *, /, () allowed"
        
        # Calculate the result
        result = eval(expression)
        
        # Format nicely for large numbers
        if isinstance(result, (int, float)):
            if result > 1000:
                return f"{result:,.2f}"
            return str(result)
            
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except Exception as e:
        return f"Error: Invalid expression"

# Create the tool
calculator = Tool(
    name="Calculator",
    func=safe_calculator,
    description="Performs mathematical calculations. Input should be a math expression like '2+2' or '100*3.14'"
)

# Test it
print(calculator.func("2 + 2"))           # "4"
print(calculator.func("1000 * 1.5"))      # "1,500.00"
print(calculator.func("10 / 0"))          # "Error: Cannot divide by zero"
print(calculator.func("hack()"))          # "Error: Only numbers and +, -, *, /, () allowed"
