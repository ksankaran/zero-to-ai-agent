# converting_to_numbers.py
# From: Zero to AI Agent, Chapter 2, Section 2.5
# Converting strings and other types to numbers

# String to integer
print("=== String to Integer ===")
user_input = "42"
number = int(user_input)
print(f"'{user_input}' converted to {number}")
print(f"Now we can do math: {number + 10}")

# String to float
print("\n=== String to Float ===")
price_input = "19.99"
price = float(price_input)
print(f"'{price_input}' converted to {price}")
print(f"With tax (10%): ${price * 1.10:.2f}")

# Float to integer (truncates, doesn't round!)
print("\n=== Float to Integer ===")
decimal = 3.7
integer = int(decimal)
print(f"{decimal} becomes {integer} (truncated, not rounded!)")

# For rounding, use round() first
rounded = int(round(decimal))
print(f"{decimal} rounded then converted: {rounded}")

# Boolean to number
print("\n=== Boolean to Number ===")
print(f"int(True) = {int(True)}")    # 1
print(f"int(False) = {int(False)}")  # 0
print(f"float(True) = {float(True)}")   # 1.0

# What CAN'T be converted (these would cause errors if uncommented)
print("\n=== Invalid Conversions (shown as comments) ===")
# bad_int = int("hello")     # Error: not a number!
# bad_int = int("12.34")     # Error: use float() first for decimals
# bad_int = int("")          # Error: empty string
print("Strings with letters, decimals, or empty strings can't convert to int directly")
