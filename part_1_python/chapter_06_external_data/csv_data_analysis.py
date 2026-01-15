# From: Zero to AI Agent, Chapter 6, Section 6.6
# File: 05_csv_data_analysis.py


import csv
from datetime import datetime
import statistics

class CSVAnalyzer:
    """Analyze and process CSV data"""
    
    def __init__(self, filename):
        self.filename = filename
        self.data = []
        self.headers = []
        self.load_data()
    
    def load_data(self):
        """Load CSV data into memory"""
        try:
            with open(self.filename, 'r') as f:
                reader = csv.DictReader(f)
                self.headers = reader.fieldnames
                self.data = list(reader)
            print(f"✅ Loaded {len(self.data)} records from {self.filename}")
        except FileNotFoundError:
            print(f"❌ File {self.filename} not found")
        except Exception as e:
            print(f"❌ Error loading file: {e}")
    
    def summary(self):
        """Show data summary"""
        if not self.data:
            print("No data loaded")
            return
        
        print(f"\n📊 DATA SUMMARY")
        print("-" * 40)
        print(f"File: {self.filename}")
        print(f"Rows: {len(self.data)}")
        print(f"Columns: {len(self.headers)}")
        print(f"Headers: {', '.join(self.headers)}")
        
        # Show sample data
        print("\nFirst 3 rows:")
        for row in self.data[:3]:
            print(f"  {row}")
    
    def analyze_column(self, column):
        """Analyze a specific column"""
        if column not in self.headers:
            print(f"❌ Column '{column}' not found")
            return
        
        values = [row[column] for row in self.data]
        
        # Try to convert to numbers
        try:
            numeric_values = [float(v) for v in values if v]
            
            print(f"\n📈 ANALYSIS: {column}")
            print("-" * 40)
            print(f"Count: {len(numeric_values)}")
            print(f"Sum: {sum(numeric_values):,.2f}")
            print(f"Mean: {statistics.mean(numeric_values):,.2f}")
            print(f"Median: {statistics.median(numeric_values):,.2f}")
            print(f"Min: {min(numeric_values):,.2f}")
            print(f"Max: {max(numeric_values):,.2f}")
            
        except (ValueError, statistics.StatisticsError):
            # Not numeric, analyze as text
            unique_values = set(values)
            print(f"\n📝 ANALYSIS: {column}")
            print("-" * 40)
            print(f"Unique values: {len(unique_values)}")
            print(f"Most common values:")
            
            from collections import Counter
            value_counts = Counter(values)
            for value, count in value_counts.most_common(5):
                print(f"  '{value}': {count} times")
    
    def filter_data(self, column, condition, value):
        """Filter data based on condition"""
        filtered = []
        
        for row in self.data:
            row_value = row.get(column, '')
            
            # Try numeric comparison
            try:
                row_val = float(row_value)
                compare_val = float(value)
                
                if condition == '>' and row_val > compare_val:
                    filtered.append(row)
                elif condition == '<' and row_val < compare_val:
                    filtered.append(row)
                elif condition == '=' and row_val == compare_val:
                    filtered.append(row)
                    
            except ValueError:
                # String comparison
                if condition == '=' and row_value == value:
                    filtered.append(row)
        
        return filtered
    
    def export_filtered(self, filtered_data, output_file):
        """Export filtered data to new CSV"""
        if not filtered_data:
            print("No data to export")
            return
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(filtered_data)
        
        print(f"✅ Exported {len(filtered_data)} records to {output_file}")

# Demo the analyzer
print("🔬 CSV DATA ANALYZER DEMO\n")

# Create sample data
sample_data = """employee_id,name,department,salary,years
101,Alice Johnson,Engineering,95000,5
102,Bob Smith,Marketing,75000,3
103,Charlie Davis,Engineering,105000,7
104,Diana Wilson,Sales,80000,4
105,Eve Martinez,Engineering,98000,6
106,Frank Brown,Marketing,72000,2
107,Grace Lee,Sales,85000,5
108,Henry Taylor,HR,70000,3"""

with open("employees.csv", "w") as f:
    f.write(sample_data)

# Analyze the data
analyzer = CSVAnalyzer("employees.csv")
analyzer.summary()
analyzer.analyze_column("salary")
analyzer.analyze_column("department")

# Filter high earners
high_earners = analyzer.filter_data("salary", ">", "90000")
print(f"\nHigh earners (>$90,000): {len(high_earners)}")
for emp in high_earners:
    print(f"  {emp['name']}: ${emp['salary']}")

# Export engineering team
engineering = analyzer.filter_data("department", "=", "Engineering")
analyzer.export_filtered(engineering, "engineering_team.csv")

# Clean up
import os
os.remove("employees.csv")
if os.path.exists("engineering_team.csv"):
    os.remove("engineering_team.csv")
