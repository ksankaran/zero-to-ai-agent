# mixing_numbers.py
# From: Zero to AI Agent, Chapter 2, Section 2.2
# When you mix int and float, you get float

int_num = 10
float_num = 3.5

result = int_num + float_num
print(f"{int_num} + {float_num} = {result}")
print(f"Type of result: {type(result)}")

# Even adding 0.0 converts to float
converted = 42 + 0.0
print(f"\n42 + 0.0 = {converted}")
print(f"Type: {type(converted)}")

# Multiple operations
calc = 10 + 5.5 * 2  # One float makes everything float
print(f"\n10 + 5.5 * 2 = {calc}")
print(f"Type: {type(calc)}")
