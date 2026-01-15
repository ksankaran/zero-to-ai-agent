# From: Zero to AI Agent, Chapter 5, Section 5.7
# File: import_examples.py

# Import entire module
import my_tools
result = my_tools.greet("Bob")

# Import specific functions
from my_tools import greet, calculate_age
result = greet("Charlie")  # No need for module name

# Import with alias
import my_tools as mt
result = mt.greet("Diana")

# Import everything (use sparingly)
from my_tools import *
result = greet("Eve")