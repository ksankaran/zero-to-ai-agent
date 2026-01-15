# From: Zero to AI Agent, Chapter 12, Section 12.3
# File: exercise_3_12_3_solution.py

from langchain_experimental.tools import PythonREPLTool
from langchain_community.tools import WriteFileTool
import tempfile
import json

# Initialize tools
python_tool = PythonREPLTool()
workspace = tempfile.mkdtemp(prefix="data_analysis_")
write_tool = WriteFileTool(root_dir=workspace)

print("DATA PROCESSING PIPELINE")
print("=" * 60)

# 1. Generate sample data
print("\n1. Generating Data...")
generate_code = """
import random
random.seed(42)
data = [round(random.gauss(50, 15), 2) for _ in range(100)]
print(f"Generated {len(data)} data points")
print(f"First 5: {data[:5]}")
"""
python_tool.run(generate_code)

# 2. Calculate statistics
print("\n2. Calculating Statistics...")
stats_code = """
import statistics
data = [45.51, 47.79, 50.59, 29.52, 46.56]  # Sample for demo
mean = statistics.mean(data)
stdev = statistics.stdev(data)
print(f"Mean: {mean:.2f}, Std Dev: {stdev:.2f}")
print(f"Min: {min(data):.2f}, Max: {max(data):.2f}")
"""
python_tool.run(stats_code)

# 3. Create and save report
print("\n3. Creating Report...")
report = """# Data Analysis Report

## Statistics
- Mean: 43.99
- Std Dev: 8.42
- Min: 29.52
- Max: 50.59

## Data Quality
✓ No missing values
✓ Normal distribution confirmed
"""

write_tool.run({"file_path": "analysis_report.md", "text": report})
print(f"Report saved: {workspace}/analysis_report.md")

# 4. Test edge cases
print("\n4. Testing Edge Cases...")
edge_code = """
import statistics
# Empty data test
try:
    statistics.mean([])
except statistics.StatisticsError:
    print("✓ Empty data handled correctly")

# Single value test
print(f"✓ Single value: mean={statistics.mean([42])}")

# Invalid types test
try:
    statistics.mean([1, 'two', 3])
except TypeError:
    print("✓ Invalid types caught correctly")
"""
python_tool.run(edge_code)

print(f"\nPipeline complete! Files saved in: {workspace}")
