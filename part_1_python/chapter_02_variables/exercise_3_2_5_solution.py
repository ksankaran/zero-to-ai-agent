# Exercise 3: Receipt Calculator
# Clean up messy price strings and calculate totals

# Solution:

print("=" * 40)
print("RECEIPT CALCULATOR")
print("=" * 40)

# Messy price data (as strings with symbols)
item1_name = "Coffee"
item1_price_str = "$4.99"

item2_name = "Sandwich"
item2_price_str = "$8.50"

item3_name = "Cookie"
item3_price_str = "$2.25"

# Clean the strings: remove $ and convert to float
item1_price = float(item1_price_str.replace("$", ""))
item2_price = float(item2_price_str.replace("$", ""))
item3_price = float(item3_price_str.replace("$", ""))

# Calculate totals
subtotal = item1_price + item2_price + item3_price
tax_rate = 0.07
tax = subtotal * tax_rate
total = subtotal + tax

# Tip suggestions
tip_15 = subtotal * 0.15
tip_20 = subtotal * 0.20

# Display cleaned receipt
print("\nOriginal (messy) prices:")
print(f"  {item1_name}: '{item1_price_str}'")
print(f"  {item2_name}: '{item2_price_str}'")
print(f"  {item3_name}: '{item3_price_str}'")

print("\nCleaned & Calculated:")
print("-" * 40)
print(f"{item1_name:<15} ${item1_price:>6.2f}")
print(f"{item2_name:<15} ${item2_price:>6.2f}")
print(f"{item3_name:<15} ${item3_price:>6.2f}")
print("-" * 40)
print(f"{'Subtotal':<15} ${subtotal:>6.2f}")
print(f"{'Tax (7%)':<15} ${tax:>6.2f}")
print(f"{'TOTAL':<15} ${total:>6.2f}")
print("-" * 40)
print(f"15% tip: ${tip_15:.2f} | 20% tip: ${tip_20:.2f}")
print("=" * 40)
