# From: Zero to AI Agent, Chapter 6, Section 6.6
# Exercise 3 Solution: Product Inventory

"""
Product Inventory
Create an inventory management system with CSV.
"""

import csv
from pathlib import Path

def create_sample_inventory():
    """Create sample inventory"""
    products = [
        ['product_name', 'quantity', 'price'],
        ['Laptop', '5', '999.99'],
        ['Mouse', '25', '19.99'],
        ['Keyboard', '15', '49.99'],
        ['Monitor', '8', '299.99'],
        ['Headphones', '3', '79.99']
    ]
    
    with open('inventory.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(products)
    print("✅ Created sample inventory.csv")

def add_product():
    """Add new product"""
    name = input("Product name: ")
    quantity = input("Quantity: ")
    price = input("Price: ")
    
    with open('inventory.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, quantity, price])
    
    print(f"✅ Added {name} to inventory")

def update_quantity():
    """Update product quantity"""
    # Read all products
    products = []
    with open('inventory.csv', 'r') as f:
        reader = csv.DictReader(f)
        products = list(reader)
    
    # Show products
    print("\n📦 Current Inventory:")
    for i, p in enumerate(products, 1):
        print(f"{i}. {p['product_name']}: {p['quantity']} units")
    
    # Get product to update
    try:
        choice = int(input("\nSelect product number: ")) - 1
        if 0 <= choice < len(products):
            new_qty = input(f"New quantity for {products[choice]['product_name']}: ")
            products[choice]['quantity'] = new_qty
            
            # Write back to file
            with open('inventory.csv', 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['product_name', 'quantity', 'price'])
                writer.writeheader()
                writer.writerows(products)
            
            print("✅ Quantity updated!")
        else:
            print("Invalid choice!")
    except ValueError:
        print("Please enter a number!")

def calculate_value():
    """Calculate total inventory value"""
    total = 0
    low_stock = []
    
    with open('inventory.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            qty = int(row['quantity'])
            price = float(row['price'])
            value = qty * price
            total += value
            
            # Check for low stock
            if qty < 10:
                low_stock.append(f"{row['product_name']} ({qty} units)")
    
    print(f"\n💰 Total Inventory Value: ${total:.2f}")
    
    if low_stock:
        print("\n⚠️ Low Stock Alert (< 10 units):")
        for item in low_stock:
            print(f"  - {item}")

def main():
    print("=== Product Inventory ===")
    
    # Create sample if needed
    if not Path('inventory.csv').exists():
        create_sample_inventory()
    
    while True:
        print("\n1. Add product")
        print("2. Update quantity")
        print("3. Calculate inventory value")
        print("4. Exit")
        
        choice = input("Choose (1-4): ")
        
        if choice == '1':
            add_product()
        elif choice == '2':
            update_quantity()
        elif choice == '3':
            calculate_value()
        elif choice == '4':
            break
    
    print("Happy managing! 📦")

if __name__ == "__main__":
    main()
