# basic_arithmetic.py
# From: Zero to AI Agent, Chapter 2, Section 2.2
# All the math operations you need

# The basics
addition = 10 + 5           # 15
subtraction = 20 - 8         # 12
multiplication = 4 * 7       # 28
division = 15 / 3            # 5.0 (note: always returns a float!)

print("10 + 5 =", addition)
print("20 - 8 =", subtraction)
print("4 * 7 =", multiplication)
print("15 / 3 =", division, "  (notice it's a float!)")

# Some operations you might not know
power = 2 ** 8               # 2 to the power of 8 = 256
floor_division = 17 // 5     # How many whole 5s in 17? Answer: 3
modulo = 17 % 5             # What's the remainder? Answer: 2

print("\n2 to the power of 8 =", power)
print("17 // 5 =", floor_division, " (floor division)")
print("17 % 5 =", modulo, " (remainder)")

# You can use parentheses to control order
result = (5 + 3) * 2         # 16 (not 11!)
print("\n(5 + 3) * 2 =", result)
