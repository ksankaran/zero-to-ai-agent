# From: Zero to AI Agent, Chapter 6, Section 6.6
# File: 01_what_are_csv.py


import csv
import os

print("📊 UNDERSTANDING CSV FILES\n")

# Let's create a simple CSV file to understand the format
print("="*50)
print("CSV FORMAT EXAMPLE:")
print("="*50)

csv_content = """name,age,city,occupation
Alice,28,New York,Data Scientist
Bob,35,San Francisco,Software Engineer
Charlie,42,Chicago,Product Manager
Diana,31,Boston,UX Designer"""

print("Raw CSV content:")
print(csv_content)

# Save it to a file
with open("example.csv", "w") as f:
    f.write(csv_content)

print("\n✅ Saved as example.csv")

# CSV files are just text!
print("\n" + "="*50)
print("CSV IS JUST TEXT:")
print("="*50)

with open("example.csv", "r") as f:
    raw_content = f.read()
    print("File content:")
    print(raw_content)

# But Python's csv module makes it powerful
print("\n" + "="*50)
print("PYTHON MAKES IT POWERFUL:")
print("="*50)

with open("example.csv", "r") as f:
    reader = csv.DictReader(f)
    print("As Python dictionaries:")
    for row in reader:
        print(f"  {row}")

# Why use CSV?
print("\n" + "="*50)
print("WHY CSV FILES?")
print("="*50)

print("""
✅ ADVANTAGES:
- Universal format (works everywhere)
- Human-readable
- Compact file size
- Fast to read/write
- Excel compatible
- Perfect for tabular data

⚠️ LIMITATIONS:
- No data types (everything is text)
- No formulas or formatting
- One table per file
- Can have delimiter conflicts
""")

# Clean up
os.remove("example.csv")
