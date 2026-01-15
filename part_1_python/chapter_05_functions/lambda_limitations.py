# From: Zero to AI Agent, Chapter 5, Section 5.5
# File: lambda_limitations.py

# Lambdas can only contain expressions, not statements

# This is OK - expression
square = lambda x: x ** 2

# This is NOT OK - print is a statement
# bad_lambda = lambda x: print(x)  # Don't do this!

# This is NOT OK - can't have multiple lines
# bad_lambda = lambda x:
#     y = x * 2  # Can't do assignments
#     return y   # Can't have multiple lines

# For anything complex, use a regular function!
def process_value(x):
    # Can have multiple lines
    print(f"Processing {x}")
    result = x * 2
    print(f"Result: {result}")
    return result