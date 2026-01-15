# Exercise 3: Receipt Formatter
# Build a formatted receipt with aligned columns

# Solution:

# Store purchase data
item1_name = "Laptop"
item1_price = 999.99
item1_qty = 1

item2_name = "Mouse"
item2_price = 29.99
item2_qty = 2

item3_name = "USB Cable"
item3_price = 9.99
item3_qty = 3

# Calculate totals
item1_total = item1_price * item1_qty
item2_total = item2_price * item2_qty
item3_total = item3_price * item3_qty

subtotal = item1_total + item2_total + item3_total
tax_rate = 0.0875  # 8.75% tax
tax_amount = subtotal * tax_rate
total = subtotal + tax_amount

# Create formatted receipt
print("=" * 50)
print("         ELECTRONIC STORE RECEIPT")
print("=" * 50)

# Using f-strings for alignment
print(f"{'Item':<20} {'Qty':>5} {'Price':>10} {'Total':>10}")
print("-" * 50)
print(f"{item1_name:<20} {item1_qty:>5} ${item1_price:>9.2f} ${item1_total:>9.2f}")
print(f"{item2_name:<20} {item2_qty:>5} ${item2_price:>9.2f} ${item2_total:>9.2f}")
print(f"{item3_name:<20} {item3_qty:>5} ${item3_price:>9.2f} ${item3_total:>9.2f}")
print("-" * 50)
print(f"{'Subtotal':>35} ${subtotal:>9.2f}")
print(f"{'Tax (8.75%)':>35} ${tax_amount:>9.2f}")
print("=" * 50)
print(f"{'TOTAL':>35} ${total:>9.2f}")
print("=" * 50)
print("\nThank you for your purchase!")
print(f"Date: 2024-03-15")
