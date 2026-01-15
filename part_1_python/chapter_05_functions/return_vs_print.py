# From: Zero to AI Agent, Chapter 5, Section 5.3
# File: return_vs_print.py

# Use RETURN when you need to use the value
def calculate_tax(amount, rate):
    return amount * rate  # Return for further use

# Use PRINT when you just want to display information
def display_welcome():
    print("=" * 40)
    print("Welcome to the Tax Calculator!")
    print("=" * 40)
    # No return needed - just displaying

# Combining both in a program
display_welcome()  # Just displays
tax = calculate_tax(100, 0.08)  # Returns value we can use
total = 100 + tax
print(f"Total with tax: ${total:.2f}")