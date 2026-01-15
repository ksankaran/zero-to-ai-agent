# From: Zero to AI Agent, Chapter 6, Section 6.6
# Exercise 2 Solution: Expense Tracker

"""
Expense Tracker
Build a simple expense tracker using CSV.
"""

import csv
from datetime import datetime

def add_expense():
    """Add a new expense"""
    date = datetime.now().strftime('%Y-%m-%d')
    description = input("Description: ")
    amount = input("Amount: ")
    category = input("Category (food/transport/other): ")
    
    # Append to CSV
    with open('expenses.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        # Write header if file is new
        if f.tell() == 0:
            writer.writerow(['date', 'description', 'amount', 'category'])
        writer.writerow([date, description, amount, category])
    
    print(f"✅ Added expense: ${amount}")

def view_expenses():
    """View all expenses"""
    try:
        with open('expenses.csv', 'r') as f:
            reader = csv.DictReader(f)
            expenses = list(reader)
            
            if not expenses:
                print("No expenses yet!")
                return
            
            print("\n💰 All Expenses:")
            for exp in expenses:
                print(f"  {exp['date']}: {exp['description']} - ${exp['amount']} ({exp['category']})")
                
    except FileNotFoundError:
        print("No expenses file found! Add an expense first.")

def calculate_by_category():
    """Calculate total by category"""
    try:
        categories = {}
        
        with open('expenses.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cat = row['category']
                amount = float(row['amount'])
                
                if cat not in categories:
                    categories[cat] = 0
                categories[cat] += amount
        
        if categories:
            print("\n📊 Expenses by Category:")
            for cat, total in categories.items():
                print(f"  {cat}: ${total:.2f}")
            
            # Save summary
            with open('summary.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['category', 'total'])
                for cat, total in categories.items():
                    writer.writerow([cat, f"{total:.2f}"])
            
            print("\n✅ Summary saved to summary.csv")
        else:
            print("No expenses to calculate!")
            
    except FileNotFoundError:
        print("No expenses file found!")

def main():
    print("=== Expense Tracker ===")
    
    while True:
        print("\n1. Add expense")
        print("2. View all expenses")
        print("3. Calculate by category")
        print("4. Exit")
        
        choice = input("Choose (1-4): ")
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            calculate_by_category()
        elif choice == '4':
            break
    
    print("Keep tracking those expenses! 💸")

if __name__ == "__main__":
    main()
