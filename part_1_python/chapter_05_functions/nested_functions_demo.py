# From: Zero to AI Agent, Chapter 5, Section 5.4
# File: nested_functions_demo.py

def outer_function(x):
    """Outer function with nested inner function"""
    
    def inner_function(y):
        # Inner function can see outer function's variables
        return x + y  # 'x' comes from enclosing scope
    
    result = inner_function(10)
    return result

print(outer_function(5))  # Prints: 15 (5 + 10)

# inner_function is not accessible here
# inner_function(10)  # Error! inner_function is local to outer_function