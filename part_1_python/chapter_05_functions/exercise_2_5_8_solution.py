# From: Zero to AI Agent, Chapter 5, Section 5.8
# Exercise 2: Shopping Cart Class

class ShoppingCart:
    """A shopping cart that manages items and calculates totals"""

    def __init__(self):
        self.items = []  # List of dictionaries with 'name' and 'price'

    def add_item(self, name, price):
        """Add an item to the cart"""
        self.items.append({"name": name, "price": price})
        print(f"Added {name} (${price:.2f}) to cart")

    def remove_item(self, name):
        """Remove an item from the cart by name"""
        for item in self.items:
            if item["name"].lower() == name.lower():
                self.items.remove(item)
                print(f"Removed {name} from cart")
                return True
        print(f"Item '{name}' not found in cart")
        return False

    def get_total(self):
        """Calculate the total price of all items"""
        total = 0
        for item in self.items:
            total += item["price"]
        return total

    def apply_discount(self, percentage):
        """Apply a discount to the total"""
        if percentage < 0 or percentage > 100:
            print("Invalid discount percentage!")
            return self.get_total()
        discount_amount = self.get_total() * (percentage / 100)
        discounted_total = self.get_total() - discount_amount
        print(f"Applied {percentage}% discount. Saved ${discount_amount:.2f}")
        return discounted_total

    def display(self):
        """Display all items in the cart"""
        print("\n" + "=" * 40)
        print("SHOPPING CART")
        print("=" * 40)
        if not self.items:
            print("Cart is empty!")
        else:
            for i, item in enumerate(self.items, 1):
                print(f"{i}. {item['name']}: ${item['price']:.2f}")
            print("-" * 40)
            print(f"Total: ${self.get_total():.2f}")
        print("=" * 40)

    def clear(self):
        """Remove all items from the cart"""
        self.items = []
        print("Cart cleared!")

    def item_count(self):
        """Return the number of items in the cart"""
        return len(self.items)


# Test the ShoppingCart class
cart = ShoppingCart()

# Add items
cart.add_item("Python Book", 39.99)
cart.add_item("Mechanical Keyboard", 89.99)
cart.add_item("USB Cable", 9.99)
cart.add_item("Mouse Pad", 14.99)

# Display cart
cart.display()

# Remove an item
print()
cart.remove_item("USB Cable")
cart.display()

# Apply discount
print()
discounted = cart.apply_discount(10)
print(f"Final total after discount: ${discounted:.2f}")

# Try to remove non-existent item
print()
cart.remove_item("Laptop")
