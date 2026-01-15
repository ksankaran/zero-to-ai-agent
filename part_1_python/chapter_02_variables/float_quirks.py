# float_quirks.py
# From: Zero to AI Agent, Chapter 2, Section 2.2
# Floating-point numbers can be weird

# This might surprise you
result = 0.1 + 0.2
print(f"0.1 + 0.2 = {result}")  # Not exactly 0.3!

# Why? Computers store decimals in binary, and some decimals
# can't be represented perfectly (like 1/3 in decimal = 0.3333...)

# For money calculations, this matters!
price = 19.99
quantity = 3
total = price * quantity
print(f"\n${price} × {quantity} = ${total}")  # Might have many decimals

# Solution: Round when displaying
print(f"Rounded: ${round(total, 2)}")

# Or format when printing
print(f"Formatted: ${total:.2f}")

# For serious money calculations, consider using integers (cents)
price_cents = 1999
quantity = 3
total_cents = price_cents * quantity
total_dollars = total_cents / 100
print(f"\nUsing cents: ${total_dollars:.2f}")
