# From: Zero to AI Agent, Chapter 5, Section 5.6
# File: import_methods.py

# Method 1: Import entire module
import math
result = math.sqrt(16)  # Need to use module name
print(f"Square root of 16: {result}")

# Method 2: Import specific functions
from math import sqrt, pi
result = sqrt(25)  # Can use directly without module name
print(f"Square root of 25: {result}")
print(f"Pi is approximately: {pi}")

# Method 3: Import everything (use sparingly!)
from math import *
result = cos(0)  # Can use any math function directly
print(f"Cosine of 0: {result}")

# Method 4: Import with an alias
import datetime as dt  # Shorter name
now = dt.datetime.now()
print(f"Current time: {now}")