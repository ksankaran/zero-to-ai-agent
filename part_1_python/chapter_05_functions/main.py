# From: Zero to AI Agent, Chapter 5, Section 5.7
# File: main_with_utils.py

# file: main.py
# Using your package
from utils import text_tools
from utils.math_tools import is_prime, fibonacci

# Use the functions
text = "  Hello   World  Python  "
cleaned = text_tools.clean_text(text)
count = text_tools.word_count(cleaned)
print(f"Cleaned: '{cleaned}'")
print(f"Word count: {count}")

# Math operations
print(f"\nIs 17 prime? {is_prime(17)}")
print(f"First 10 Fibonacci numbers: {fibonacci(10)}")