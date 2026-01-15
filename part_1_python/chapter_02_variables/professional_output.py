# professional_output.py
# From: Zero to AI Agent, Chapter 2, Section 2.6
# Creating beautiful, formatted output

# Basic formatting with f-strings
name = "Alice"
balance = 1234.56789
print(f"Customer: {name}")
print(f"Balance: ${balance:.2f}")  # 2 decimal places

# Alignment in f-strings
print("\n=== Product List ===")
print(f"{'Item':<20} {'Price':>10}")
print("-" * 30)
print(f"{'Apple':<20} {'$2.99':>10}")
print(f"{'Banana':<20} {'$1.99':>10}")
print(f"{'Orange':<20} {'$3.49':>10}")

# Number formatting
number = 1234567.89
print("\n=== Number Formats ===")
print(f"Default: {number}")
print(f"Comma separator: {number:,}")
print(f"Two decimals: {number:.2f}")
print(f"Percentage: {0.856:.1%}")
print(f"Scientific: {number:.2e}")

# Creating a simple report
print("\n" + "="*40)
print("DAILY SALES REPORT")
print("="*40)

# Monday's sales
mon_sales = 1250.50
# Tuesday's sales
tue_sales = 980.75
# Wednesday's sales
wed_sales = 1420.00

total = mon_sales + tue_sales + wed_sales
average = total / 3

print(f"Monday:    ${mon_sales:>10.2f}")
print(f"Tuesday:   ${tue_sales:>10.2f}")
print(f"Wednesday: ${wed_sales:>10.2f}")
print("-"*40)
print(f"Total:     ${total:>10.2f}")
print(f"Average:   ${average:>10.2f}")
