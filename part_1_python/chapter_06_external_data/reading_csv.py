# From: Zero to AI Agent, Chapter 6, Section 6.6
# File: 02_reading_csv.py


import csv

print("📖 READING CSV FILES\n")

# First, create a sample CSV file with different types of data
sample_data = """product_id,product_name,price,quantity,in_stock
1001,Laptop,999.99,50,TRUE
1002,Mouse,19.99,200,TRUE
1003,Keyboard,79.99,0,FALSE
1004,"Monitor, HD",299.99,25,TRUE
1005,"USB Cable (6ft)",9.99,500,TRUE"""

with open("products.csv", "w") as f:
    f.write(sample_data)

# Method 1: Basic reader (returns lists)
print("="*50)
print("METHOD 1: Basic CSV Reader (Lists)")
print("="*50)

with open("products.csv", "r") as f:
    reader = csv.reader(f)
    
    # First row is usually headers
    headers = next(reader)
    print(f"Headers: {headers}")
    
    print("\nData rows:")
    for row in reader:
        print(f"  {row}")

# Method 2: DictReader (returns dictionaries)
print("\n" + "="*50)
print("METHOD 2: DictReader (Dictionaries)")
print("="*50)

with open("products.csv", "r") as f:
    reader = csv.DictReader(f)
    
    print("Each row as a dictionary:")
    for row in reader:
        name = row['product_name']
        price = float(row['price'])
        in_stock = row['in_stock'] == 'TRUE'
        print(f"  {name}: ${price:.2f} ({'In Stock' if in_stock else 'Out of Stock'})")

# Method 3: Reading into memory
print("\n" + "="*50)
print("METHOD 3: Load Everything into Memory")
print("="*50)

with open("products.csv", "r") as f:
    reader = csv.DictReader(f)
    products = list(reader)  # Convert to list

print(f"Loaded {len(products)} products")

# Now we can process the data
total_value = sum(float(p['price']) * int(p['quantity']) for p in products)
in_stock_count = sum(1 for p in products if p['in_stock'] == 'TRUE')

print(f"Total inventory value: ${total_value:,.2f}")
print(f"Products in stock: {in_stock_count}/{len(products)}")

# Handling different delimiters
print("\n" + "="*50)
print("HANDLING DIFFERENT DELIMITERS")
print("="*50)

# Create a tab-separated file
tsv_data = "name\tage\tcity\nAlice\t28\tNYC\nBob\t35\tSF"
with open("data.tsv", "w") as f:
    f.write(tsv_data)

# Read with custom delimiter
with open("data.tsv", "r") as f:
    reader = csv.reader(f, delimiter='\t')
    print("Tab-separated data:")
    for row in reader:
        print(f"  {row}")

# Clean up
import os
os.remove("products.csv")
os.remove("data.tsv")
