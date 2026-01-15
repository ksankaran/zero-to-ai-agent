# From: Zero to AI Agent, Chapter 4, Section 4.4
# Exercise 1: Product Inventory System

# Store products
inventory = {
    "laptop": {"price": 999.99, "quantity": 5},
    "mouse": {"price": 29.99, "quantity": 15},
    "keyboard": {"price": 79.99, "quantity": 8}
}

# Add new product
inventory["monitor"] = {"price": 299.99, "quantity": 3}
print("Added monitor to inventory")

# Update quantities
inventory["laptop"]["quantity"] += 2
print(f"Updated laptop quantity: {inventory['laptop']['quantity']}")

# Calculate total value
total_value = sum(
    product["price"] * product["quantity"] 
    for product in inventory.values()
)
print(f"Total inventory value: ${total_value:.2f}")

# Find low stock (below 5)
low_stock = [
    name for name, product in inventory.items() 
    if product["quantity"] < 5
]
print(f"Products low in stock: {low_stock}")

# Generate restock report
print("\nRestock Report:")
for name, product in inventory.items():
    if product["quantity"] < 5:
        needed = 10 - product["quantity"]
        print(f"  {name}: Order {needed} units")
