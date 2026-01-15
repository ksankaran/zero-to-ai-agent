# From: Zero to AI Agent, Chapter 6, Section 6.6
# File: 04_processing_large_csv.py


import csv
import time
from datetime import datetime, timedelta
import random

print("🚀 PROCESSING LARGE CSV FILES\n")

# Create a large CSV file for demonstration
print("="*50)
print("CREATING LARGE DATASET:")
print("="*50)

print("Generating 10,000 sales records...")

with open("large_sales.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['date', 'product', 'quantity', 'price', 'customer_id'])
    
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Cable']
    start_date = datetime(2024, 1, 1)
    
    for i in range(10000):
        date = (start_date + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        product = random.choice(products)
        quantity = random.randint(1, 10)
        price = random.uniform(10, 1000)
        customer_id = random.randint(1000, 9999)
        
        writer.writerow([date, product, quantity, price, customer_id])
        
        if (i + 1) % 2000 == 0:
            print(f"  Generated {i + 1} records...")

print("✅ Created large_sales.csv with 10,000 records")

# Method 1: Process line by line (memory efficient)
print("\n" + "="*50)
print("METHOD 1: Line-by-Line Processing (Memory Efficient)")
print("="*50)

start_time = time.time()
total_revenue = 0
product_counts = {}

with open("large_sales.csv", "r") as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        # Process each row without loading all into memory
        revenue = int(row['quantity']) * float(row['price'])
        total_revenue += revenue
        
        product = row['product']
        product_counts[product] = product_counts.get(product, 0) + int(row['quantity'])

elapsed = time.time() - start_time

print(f"Processing time: {elapsed:.2f} seconds")
print(f"Total revenue: ${total_revenue:,.2f}")
print("Product quantities sold:")
for product, count in sorted(product_counts.items()):
    print(f"  {product}: {count} units")

# Method 2: Chunk processing
print("\n" + "="*50)
print("METHOD 2: Chunk Processing")
print("="*50)

def process_csv_in_chunks(filename, chunk_size=1000):
    """Process CSV file in chunks"""
    chunk = []
    chunk_count = 0
    
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            chunk.append(row)
            
            if len(chunk) >= chunk_size:
                # Process this chunk
                chunk_revenue = sum(
                    int(r['quantity']) * float(r['price']) 
                    for r in chunk
                )
                chunk_count += 1
                print(f"  Processed chunk {chunk_count} (${chunk_revenue:,.2f})")
                chunk = []
        
        # Process remaining records
        if chunk:
            chunk_revenue = sum(
                int(r['quantity']) * float(r['price']) 
                for r in chunk
            )
            print(f"  Processed final chunk (${chunk_revenue:,.2f})")

process_csv_in_chunks("large_sales.csv", chunk_size=2000)

# Method 3: Filtering while reading
print("\n" + "="*50)
print("METHOD 3: Filtering While Reading")
print("="*50)

# Find high-value transactions (> $500)
high_value_count = 0
high_value_total = 0

with open("large_sales.csv", "r") as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        transaction_value = int(row['quantity']) * float(row['price'])
        
        if transaction_value > 500:
            high_value_count += 1
            high_value_total += transaction_value

print(f"High-value transactions (>$500): {high_value_count}")
print(f"Total value of high-value transactions: ${high_value_total:,.2f}")

# Clean up
import os
os.remove("large_sales.csv")
