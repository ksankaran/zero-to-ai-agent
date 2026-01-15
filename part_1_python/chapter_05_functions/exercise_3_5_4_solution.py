# From: Zero to AI Agent, Chapter 5, Section 5.4
# File: exercise_3_5_4_solution.py

# Fixed version - no global variables, proper parameter passing

def calculate_total(subtotal, tax_rate):
    """Calculate total with tax"""
    tax = subtotal * tax_rate
    total = subtotal + tax
    return total

def apply_discount(total, discount_percent):
    """Apply discount to total"""
    discount_amount = total * discount_percent
    discounted_total = total - discount_amount
    return discounted_total

def process_order(subtotal, tax_rate, discount_percent=0):
    """Process complete order"""
    # Calculate total with tax
    total_with_tax = calculate_total(subtotal, tax_rate)
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"After tax ({tax_rate*100}%): ${total_with_tax:.2f}")
    
    # Apply discount if any
    if discount_percent > 0:
        final_total = apply_discount(total_with_tax, discount_percent)
        print(f"After discount ({discount_percent*100}%): ${final_total:.2f}")
    else:
        final_total = total_with_tax
    
    return final_total

# Use the fixed functions
subtotal = 100
tax_rate = 0.08
discount = 0.1  # 10% discount

final_total = process_order(subtotal, tax_rate, discount)
print(f"Final total: ${final_total:.2f}")

# Alternative: chain the functions manually
total_with_tax = calculate_total(100, 0.08)
final_total = apply_discount(total_with_tax, 0.1)
print(f"\nAlternative calculation: ${final_total:.2f}")