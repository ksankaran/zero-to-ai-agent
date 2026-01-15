# From: Zero to AI Agent, Chapter 6, Section 6.4
# Exercise 1 Solution: Safe Calculator

"""
Safe Calculator
Create a calculator that handles errors gracefully.
"""

def safe_calculator():
    """Calculator with error handling"""
    while True:
        try:
            # Get first number
            num1 = float(input("\nEnter first number: "))
            
            # Get operation
            operation = input("Enter operation (+, -, *, /): ")
            
            # Get second number
            num2 = float(input("Enter second number: "))
            
            # Perform calculation
            if operation == '+':
                result = num1 + num2
            elif operation == '-':
                result = num1 - num2
            elif operation == '*':
                result = num1 * num2
            elif operation == '/':
                # Check for division by zero
                if num2 == 0:
                    raise ZeroDivisionError("Cannot divide by zero!")
                result = num1 / num2
            else:
                print("❌ Invalid operation! Use +, -, *, or /")
                continue
            
            # Show result
            print(f"\n✅ Result: {num1} {operation} {num2} = {result}")
            break
            
        except ValueError:
            print("❌ Please enter valid numbers!")
            print("Let's try again...")
            
        except ZeroDivisionError as e:
            print(f"❌ Math error: {e}")
            print("Let's try again...")

def main():
    print("=== Safe Calculator ===")
    
    while True:
        safe_calculator()
        
        again = input("\nCalculate again? (yes/no): ")
        if again.lower() != 'yes':
            break
    
    print("Thanks for calculating! 🧮")

if __name__ == "__main__":
    main()
