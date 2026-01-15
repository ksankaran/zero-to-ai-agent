# From: Zero to AI Agent, Chapter 5, Section 5.2
# File: exercise_3_5_2_solution.py

def calculate_total(items_list, tax_rate=0.08, discount_percent=0):
    """Calculate shopping cart total with tax and discounts"""
    print("🛒 SHOPPING CART CALCULATOR")
    print("=" * 40)
    
    # Display items
    print("\nItems:")
    for i, price in enumerate(items_list, 1):
        print(f"  Item {i}: ${price:.2f}")
    
    # Calculate subtotal
    subtotal = sum(items_list)
    print(f"\nSubtotal: ${subtotal:.2f}")
    
    # Apply discount if any
    discount_amount = 0
    if discount_percent > 0:
        discount_amount = subtotal * (discount_percent / 100)
        print(f"Discount ({discount_percent}%): -${discount_amount:.2f}")
        subtotal_after_discount = subtotal - discount_amount
    else:
        subtotal_after_discount = subtotal
    
    # Calculate tax
    tax_amount = subtotal_after_discount * tax_rate
    print(f"Tax ({tax_rate * 100:.1f}%): ${tax_amount:.2f}")
    
    # Calculate final total
    final_total = subtotal_after_discount + tax_amount
    
    print("-" * 40)
    print(f"TOTAL: ${final_total:.2f}")
    print("=" * 40)
    
    return final_total

# Test with different scenarios
prices1 = [19.99, 34.50, 12.75]
calculate_total(prices1)

print("\n")
prices2 = [50.00, 25.00, 75.00]
calculate_total(prices2, discount_percent=20)  # 20% off sale!

print("\n")
prices3 = [10.00, 10.00, 10.00]
calculate_total(prices3, tax_rate=0.10, discount_percent=10)  # Different tax, with discount
