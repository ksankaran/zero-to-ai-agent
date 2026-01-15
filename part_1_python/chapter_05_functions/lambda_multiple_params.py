# From: Zero to AI Agent, Chapter 5, Section 5.5
# File: lambda_multiple_params.py

# Regular function
def add(x, y):
    return x + y

# Lambda version
add_lambda = lambda x, y: x + y

print(add(3, 5))         # 8
print(add_lambda(3, 5))  # 8

# Or use it directly without storing
result = (lambda x, y: x + y)(10, 20)
print(result)  # 30