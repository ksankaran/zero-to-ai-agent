# From: Zero to AI Agent, Chapter 5, Section 5.5
# File: exercise_2_5_5_solution.py

products = [
    {"name": "Laptop", "price": 1200, "stock": 5},
    {"name": "Mouse", "price": 25, "stock": 50},
    {"name": "Keyboard", "price": 75, "stock": 30},
    {"name": "Monitor", "price": 300, "stock": 10}
]

# 1. Sort by price (lowest to highest)
by_price = sorted(products, key=lambda p: p["price"])
print("Sorted by price:")
for product in by_price:
    print(f"  ${product['price']:6} - {product['name']}")

# 2. Sort by name (alphabetically)
by_name = sorted(products, key=lambda p: p["name"])
print("\nSorted by name:")
for product in by_name:
    print(f"  {product['name']:10} - ${product['price']}")

# 3. Find most expensive product
most_expensive = max(products, key=lambda p: p["price"])
print(f"\nMost expensive: {most_expensive['name']} at ${most_expensive['price']}")

# Bonus: Find products with low stock
low_stock = list(filter(lambda p: p["stock"] < 20, products))
print(f"\nLow stock items:")
for product in low_stock:
    print(f"  {product['name']}: only {product['stock']} left")