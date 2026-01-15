# order_of_operations.py
# From: Zero to AI Agent, Chapter 2, Section 2.2
# Python follows PEMDAS

# Without parentheses
result1 = 2 + 3 * 4    # 14 (not 20!)
print("2 + 3 * 4 =", result1)
print("Python does: 2 + (3 * 4) = 2 + 12 = 14")

# With parentheses to change order
result2 = (2 + 3) * 4  # 20
print("\n(2 + 3) * 4 =", result2)

# A more complex example
complex_calc = 100 - 10 ** 2 + 5 * 3
print("\n100 - 10 ** 2 + 5 * 3 =", complex_calc)
print("Step by step:")
print("1. 10 ** 2 = 100")
print("2. 5 * 3 = 15")
print("3. 100 - 100 = 0")
print("4. 0 + 15 = 15")

# When in doubt, use parentheses!
clear_calc = 100 - (10 ** 2) + (5 * 3)  # Same result, but clearer
