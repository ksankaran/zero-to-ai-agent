# Exercise 2: Shopping Calculator
# Create variables for keyboard ($79.99), mouse ($45.50), and monitor ($299.99)
# Calculate subtotal, tax (8%), and final total

# Solution:

# Store item prices
keyboard_price = 79.99
mouse_price = 45.50
monitor_price = 299.99

# Calculate subtotal
subtotal = keyboard_price + mouse_price + monitor_price

# Calculate tax (8%)
tax_rate = 0.08
tax_amount = subtotal * tax_rate

# Calculate final total
total = subtotal + tax_amount

# Display the results
print("Shopping Cart Summary")
print("=" * 40)
print("Keyboard: $", keyboard_price)
print("Mouse: $", mouse_price)
print("Monitor: $", monitor_price)
print("-" * 40)
print("Subtotal: $", subtotal)
print("Tax (8%): $", tax_amount)
print("Total: $", total)

# Alternative with better formatting (rounding to 2 decimal places)
print("\n--- Formatted Version ---")
print("Subtotal: $", round(subtotal, 2))
print("Tax: $", round(tax_amount, 2))
print("Total: $", round(total, 2))
