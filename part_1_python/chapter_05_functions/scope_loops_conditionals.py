# From: Zero to AI Agent, Chapter 5, Section 5.4
# File: scope_loops_conditionals.py

# Variables in if statements are accessible outside
if True:
    message = "This is accessible outside the if!"
print(message)  # Works fine!

# Variables in loops are accessible outside
for i in range(3):
    loop_variable = f"Loop iteration {i}"
print(loop_variable)  # Prints: Loop iteration 2
print(i)  # Prints: 2 (the last value)

# But functions DO create their own scope
def my_function():
    function_variable = "Only exists in here"
# print(function_variable)  # Error! Not accessible