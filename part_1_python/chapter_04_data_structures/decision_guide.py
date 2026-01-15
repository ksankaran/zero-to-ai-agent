# From: Zero to AI Agent, Chapter 4, Section 4.6
# decision_guide.py - Quick decision guide for choosing data structures

# THE GOLDEN QUESTIONS TO ASK YOURSELF:

# 1. Do I need to store key-value pairs or look things up by name?
#    → Use a DICTIONARY
user = {"name": "Alice", "age": 30, "email": "alice@example.com"}

# 2. Do I need to ensure uniqueness or perform set operations?
#    → Use a SET
unique_visitors = {"user123", "user456", "user789"}

# 3. Will this data never change once created?
#    → Use a TUPLE
coordinates = (40.7128, -74.0060)  # NYC coordinates won't change

# 4. Do I need an ordered, changeable collection?
#    → Use a LIST
shopping_cart = ["apples", "bread", "milk"]
