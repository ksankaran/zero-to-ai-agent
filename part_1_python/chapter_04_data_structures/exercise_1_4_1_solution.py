# From: Zero to AI Agent, Chapter 4, Section 4.1
# Exercise 1: Shopping Cart Manager

# 1. Start with an empty cart
cart = []
print("Starting with empty cart:", cart)

# 2. Add items
items_to_add = ["apples", "bread", "milk", "eggs", "cheese"]
for item in items_to_add:
    cart.append(item)
print("Cart after adding items:", cart)

# 3. Display first and last items
print(f"First item: {cart[0]}")
print(f"Last item: {cart[-1]}")

# 4. Remove the third item (index 2)
removed_item = cart.pop(2)
print(f"Removed item: {removed_item}")
print("Cart after removal:", cart)

# 5. Check if "milk" is in cart
has_milk = "milk" in cart
print(f"Is 'milk' in cart? {has_milk}")

# 6. Display total number of items
total_items = len(cart)
print(f"Total items in cart: {total_items}")
print("Final cart:", cart)
