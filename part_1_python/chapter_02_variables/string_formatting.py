# string_formatting.py
# From: Zero to AI Agent, Chapter 2, Section 2.3
# Making your output look professional

# Basic f-string formatting
name = "Alice"
balance = 1234.56789
print(f"Customer: {name}")
print(f"Balance: ${balance:.2f}")  # 2 decimal places

# Padding and alignment
print("\n--- Alignment ---")
print(f"{'Left':<10} | {'Center':^10} | {'Right':>10}")
print(f"{'─'*10} | {'─'*10} | {'─'*10}")
print(f"{'Apple':<10} | {'$4.99':^10} | {'15':>10}")
print(f"{'Banana':<10} | {'$2.99':^10} | {'23':>10}")
print(f"{'Orange':<10} | {'$3.49':^10} | {'18':>10}")

# Number formatting
number = 1234567.89
print("\n--- Number Formatting ---")
print(f"Default: {number}")
print(f"Comma separator: {number:,.2f}")
print(f"Percentage: {0.856:.1%}")
print(f"Scientific: {number:.2e}")

# Creating a formatted mini-report
print("\n" + "="*50)
print(f"{'SALES SUMMARY':^50}")
print("="*50)

item1 = "Laptop"
price1 = 999.99
qty1 = 5
total1 = price1 * qty1

item2 = "Mouse"
price2 = 24.99
qty2 = 15
total2 = price2 * qty2

item3 = "Keyboard"
price3 = 79.99
qty3 = 8
total3 = price3 * qty3

print(f"{'Item':<20} {'Price':>10} {'Qty':>5} {'Total':>10}")
print("-"*50)
print(f"{item1:<20} ${price1:>9.2f} {qty1:>5} ${total1:>9.2f}")
print(f"{item2:<20} ${price2:>9.2f} {qty2:>5} ${total2:>9.2f}")
print(f"{item3:<20} ${price3:>9.2f} {qty3:>5} ${total3:>9.2f}")
print("-"*50)

grand_total = total1 + total2 + total3
print(f"{'GRAND TOTAL':>35}: ${grand_total:>9.2f}")
