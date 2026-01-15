# From: Zero to AI Agent, Chapter 5, Section 5.6
# File: module_help_demo.py

import math

# See all functions in a module
print("Math module functions:")
print(dir(math)[:10])  # Show first 10

# Get help on a specific function
help(math.sqrt)  # Shows documentation

# In Jupyter or interactive Python, use ? or ??
# math.sqrt?  # Shows quick help
# math.sqrt??  # Shows source code

# Check module location
print(f"Math module is located at: {math.__file__}")