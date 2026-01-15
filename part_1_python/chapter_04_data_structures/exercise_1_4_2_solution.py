# From: Zero to AI Agent, Chapter 4, Section 4.2
# Exercise 1: Shopping Cart Manager

# 1. Start with empty cart
cart = []
print("Starting cart:", cart)

# 2. Add items
items = ["apple", "banana", "apple", "orange", "banana", "grape"]
for item in items:
    cart.append(item)
print("Cart with items:", cart)

# 3. Count apples and bananas
apple_count = cart.count("apple")
banana_count = cart.count("banana")
print(f"Apples: {apple_count}, Bananas: {banana_count}")

# 4. Remove one banana
cart.remove("banana")
print("After removing one banana:", cart)

# 5. Sort alphabetically
cart.sort()
print("Sorted cart:", cart)

# 6. Display final cart and total
print(f"Final cart: {cart}")
print(f"Total items: {len(cart)}")
