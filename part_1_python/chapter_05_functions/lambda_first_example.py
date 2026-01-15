# From: Zero to AI Agent, Chapter 5, Section 5.5
# File: lambda_first_example.py

# Regular function
def double(x):
    return x * 2

# Lambda function - same thing!
double_lambda = lambda x: x * 2

# They work the same way
print(double(5))        # 10
print(double_lambda(5)) # 10