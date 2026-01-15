# From: Zero to AI Agent, Chapter 5, Section 5.3
# File: print_problem.py

# A function that only prints
def add_numbers_bad(x, y):
    result = x + y
    print(f"{x} + {y} = {result}")

# Try to use the result
total = add_numbers_bad(5, 3)
print(f"The total is {total}")