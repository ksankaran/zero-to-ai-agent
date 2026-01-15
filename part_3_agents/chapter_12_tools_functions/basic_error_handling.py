# From: Zero to AI Agent, Chapter 12, Section 12.6
# File: basic_error_handling.py

from langchain_core.tools import Tool

# ❌ BAD: Tool that crashes
def bad_calculator(expression: str) -> str:
    result = eval(expression)  # This will crash on bad input!
    return str(result)

# ✅ GOOD: Tool that handles errors
def good_calculator(expression: str) -> str:
    try:
        result = eval(expression)
        return str(result)
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except SyntaxError:
        return "Error: Invalid mathematical expression"
    except Exception as e:
        return f"Error: Calculation failed - {str(e)}"

# Test both versions
test_cases = [
    "10 + 5",      # Works fine
    "10 / 0",      # Division by zero
    "10 +",        # Syntax error
    "hello",       # Name error
]

print("COMPARING ERROR HANDLING")
print("=" * 50)

# Create tools
bad_tool = Tool(name="BadCalc", func=bad_calculator, description="Unsafe calculator")
good_tool = Tool(name="GoodCalc", func=good_calculator, description="Safe calculator")

for expression in test_cases:
    print(f"\nTesting: {expression}")
    
    # Try bad tool (wrapped to catch crashes)
    try:
        bad_result = bad_tool.func(expression)
        print(f"  Bad tool: {bad_result}")
    except Exception as e:
        print(f"  Bad tool: 💥 CRASHED - {e}")
    
    # Good tool always returns something
    good_result = good_tool.func(expression)
    print(f"  Good tool: {good_result}")
