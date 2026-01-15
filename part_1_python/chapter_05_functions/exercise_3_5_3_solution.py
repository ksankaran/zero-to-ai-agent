# From: Zero to AI Agent, Chapter 5, Section 5.3
# File: exercise_3_5_3_solution.py

def calculate_item_total(price, quantity):
    """Calculate total for a single item"""
    return price * quantity

def apply_discount(total, discount_percent):
    """Apply percentage discount to total"""
    discount_amount = total * (discount_percent / 100)
    return total - discount_amount

def calculate_tax(subtotal, tax_rate):
    """Calculate tax amount"""
    return subtotal * tax_rate

def calculate_final_total(items_list, discount_percent=0, tax_rate=0.08):
    """Calculate final total for shopping cart"""
    # Calculate sum of all items
    items_total = 0
    print("\n🛒 SHOPPING CART BREAKDOWN 🛒")
    print("-" * 40)
    
    for item_name, price, quantity in items_list:
        item_total = calculate_item_total(price, quantity)
        items_total += item_total
        print(f"{item_name}: ${price:.2f} × {quantity} = ${item_total:.2f}")
    
    print("-" * 40)
    print(f"Items Total: ${items_total:.2f}")
    
    # Apply discount if any
    if discount_percent > 0:
        subtotal = apply_discount(items_total, discount_percent)
        discount_amount = items_total - subtotal
        print(f"Discount ({discount_percent}%): -${discount_amount:.2f}")
        print(f"Subtotal: ${subtotal:.2f}")
    else:
        subtotal = items_total
    
    # Calculate tax
    tax = calculate_tax(subtotal, tax_rate)
    print(f"Tax ({tax_rate*100:.1f}%): +${tax:.2f}")
    
    # Calculate final total
    final = subtotal + tax
    print("-" * 40)
    print(f"FINAL TOTAL: ${final:.2f}")
    
    return final

# Test the shopping cart
cart = [
    ("Apple", 1.50, 3),
    ("Banana", 0.75, 6),
    ("Orange", 2.00, 2),
    ("Milk", 3.50, 1)
]

# Without discount
total1 = calculate_final_total(cart)

# With 10% discount
print("\n")
total2 = calculate_final_total(cart, discount_percent=10, tax_rate=0.0825)

# Store the result for further use
if total2 < 20:
    print(f"\n✨ Great deal! You spent under $20!")
else:
    print(f"\n📝 Your total of ${total2:.2f} has been saved.")