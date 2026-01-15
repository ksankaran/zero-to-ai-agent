# modulo_magic.py
# From: Zero to AI Agent, Chapter 2, Section 2.2
# The modulo operator (%) returns the remainder after division

print("=" * 40)
print("THE MODULO OPERATOR (%)")
print("=" * 40)

# Basic modulo examples
print("10 % 3 =", 10 % 3)   # 1 (10 divided by 3 = 3 remainder 1)
print("17 % 5 =", 17 % 5)   # 2 (17 divided by 5 = 3 remainder 2)
print("20 % 4 =", 20 % 4)   # 0 (20 divided by 4 = 5 remainder 0)

# Practical example: Converting seconds to minutes and seconds
print("")
print("=" * 40)
print("CONVERTING TIME")
print("=" * 40)

total_seconds = 185
minutes = total_seconds // 60    # Integer division gives whole minutes
remaining_seconds = total_seconds % 60   # Modulo gives remaining seconds

print(f"Total seconds: {total_seconds}")
print(f"Minutes: {minutes}")
print(f"Remaining seconds: {remaining_seconds}")
print(f"So {total_seconds} seconds = {minutes} minutes and {remaining_seconds} seconds")

# Even/odd check - the result tells us!
print("")
print("=" * 40)
print("EVEN OR ODD?")
print("=" * 40)

number1 = 17
number2 = 24

remainder1 = number1 % 2
remainder2 = number2 % 2

print(f"{number1} % 2 = {remainder1}")
print(f"(If remainder is 0, it's even. If 1, it's odd.)")
print("")
print(f"{number2} % 2 = {remainder2}")
print(f"(If remainder is 0, it's even. If 1, it's odd.)")
print("=" * 40)
