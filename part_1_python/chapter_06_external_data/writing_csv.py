# From: Zero to AI Agent, Chapter 6, Section 6.6
# File: 03_writing_csv.py


import csv
from datetime import datetime

print("✏️ WRITING CSV FILES\n")

# Method 1: Basic writer
print("="*50)
print("METHOD 1: Basic CSV Writer")
print("="*50)

data = [
    ['name', 'department', 'salary'],
    ['Alice Johnson', 'Engineering', 95000],
    ['Bob Smith', 'Marketing', 75000],
    ['Charlie Davis', 'Sales', 80000]
]

with open("employees.csv", "w", newline='') as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)

print("✅ Created employees.csv")

# Method 2: DictWriter (cleaner for structured data)
print("\n" + "="*50)
print("METHOD 2: DictWriter")
print("="*50)

orders = [
    {'order_id': 1001, 'customer': 'Alice', 'amount': 250.50, 'date': '2024-01-15'},
    {'order_id': 1002, 'customer': 'Bob', 'amount': 180.00, 'date': '2024-01-16'},
    {'order_id': 1003, 'customer': 'Charlie', 'amount': 420.75, 'date': '2024-01-17'},
]

with open("orders.csv", "w", newline='') as f:
    fieldnames = ['order_id', 'customer', 'amount', 'date']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    # Write header row
    writer.writeheader()
    
    # Write data rows
    for order in orders:
        writer.writerow(order)

print("✅ Created orders.csv")

# Method 3: Appending to existing CSV
print("\n" + "="*50)
print("METHOD 3: Appending Data")
print("="*50)

new_order = {'order_id': 1004, 'customer': 'Diana', 'amount': 150.25, 'date': '2024-01-18'}

with open("orders.csv", "a", newline='') as f:
    fieldnames = ['order_id', 'customer', 'amount', 'date']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writerow(new_order)

print("✅ Appended new order to orders.csv")

# Verify the files
print("\n" + "="*50)
print("VERIFYING FILES CREATED:")
print("="*50)

for filename in ["employees.csv", "orders.csv"]:
    with open(filename, "r") as f:
        lines = f.readlines()
        print(f"\n{filename} ({len(lines)} lines):")
        for line in lines[:3]:  # Show first 3 lines
            print(f"  {line.strip()}")

# Clean up
import os
os.remove("employees.csv")
os.remove("orders.csv")
