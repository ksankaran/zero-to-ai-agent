# From: Zero to AI Agent, Chapter 4 Challenge Project
# datamaster.py - Your Personal Data Analysis System
# A data analysis challenge using all Python data structures (without classes or functions)

print("=" * 50)
print("DATAMASTER - Personal Data Analysis System")
print("=" * 50)
print("")
print("This is a CHALLENGE PROJECT!")
print("Try to implement these features using what you've learned.")
print("")

# Initialize your data structures
datasets = {}  # Dictionary to store named datasets
unique_values = set()  # Track all unique values seen
history = []  # List of operations performed
metadata = {}  # Dictionary for dataset information
cache = {}  # Dictionary for cached results

# Sample data to work with
print("Loading sample sales data...")
sales_data = [
    {"id": 1, "product": "Widget A", "price": 29.99, "quantity": 10, "region": "North"},
    {"id": 2, "product": "Widget B", "price": 49.99, "quantity": 5, "region": "South"},
    {"id": 3, "product": "Widget A", "price": 29.99, "quantity": 8, "region": "East"},
    {"id": 4, "product": "Widget C", "price": 19.99, "quantity": 20, "region": "North"},
    {"id": 5, "product": "Widget B", "price": 49.99, "quantity": 3, "region": "West"},
]

datasets["sales"] = sales_data
metadata["sales"] = {"rows": len(sales_data), "source": "sample"}
history.append(("import", "sales", "5 records"))
print(f"Loaded {len(sales_data)} sales records")
print("")

# CHALLENGE 1: Get unique products
print("CHALLENGE 1: Find unique products")
print("-" * 40)
# Use a set to find unique products
unique_products = {record["product"] for record in sales_data}
print(f"Unique products: {unique_products}")
print("")

# CHALLENGE 2: Calculate total revenue by product
print("CHALLENGE 2: Total revenue by product")
print("-" * 40)
# Use a dictionary to accumulate totals
revenue_by_product = {}
for record in sales_data:
    product = record["product"]
    revenue = record["price"] * record["quantity"]
    revenue_by_product[product] = revenue_by_product.get(product, 0) + revenue

for product, revenue in revenue_by_product.items():
    print(f"  {product}: ${revenue:.2f}")
print("")

# CHALLENGE 3: Group sales by region
print("CHALLENGE 3: Sales by region")
print("-" * 40)
# Use dictionary with lists as values
sales_by_region = {}
for record in sales_data:
    region = record["region"]
    if region not in sales_by_region:
        sales_by_region[region] = []
    sales_by_region[region].append(record)

for region, records in sales_by_region.items():
    print(f"  {region}: {len(records)} sales")
print("")

# CHALLENGE 4: Find records with high quantities using list comprehension
print("CHALLENGE 4: High quantity sales (quantity > 5)")
print("-" * 40)
high_quantity_sales = [record for record in sales_data if record["quantity"] > 5]
for sale in high_quantity_sales:
    print(f"  {sale['product']}: {sale['quantity']} units")
print("")

# CHALLENGE 5: Calculate statistics
print("CHALLENGE 5: Price statistics")
print("-" * 40)
prices = [record["price"] for record in sales_data]
prices_sorted = sorted(prices)

total_price = 0
for p in prices:
    total_price = total_price + p

min_price = prices_sorted[0]
max_price = prices_sorted[-1]
avg_price = total_price / len(prices)

print(f"  Minimum price: ${min_price:.2f}")
print(f"  Maximum price: ${max_price:.2f}")
print(f"  Average price: ${avg_price:.2f}")
print("")

# Show operation history
print("=" * 50)
print("OPERATION HISTORY")
print("=" * 50)
for operation, dataset, details in history:
    print(f"  [{operation}] {dataset}: {details}")

print("")
print("=" * 50)
print("YOUR CHALLENGES:")
print("=" * 50)
print("1. Add more data to the datasets dictionary")
print("2. Create a query system using list comprehensions")
print("3. Implement a caching system for expensive operations")
print("4. Add customer data and find correlations with sales")
print("5. Generate a comprehensive report using all data structures")
print("=" * 50)
