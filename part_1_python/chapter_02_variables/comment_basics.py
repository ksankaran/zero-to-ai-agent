# comment_basics.py
# From: Zero to AI Agent, Chapter 2, Section 2.7
# This is a single-line comment - Python ignores everything after the #

# Comments explain WHY, not just WHAT
age = 25  # User's age in years (not months or days)

# BAD comment (states the obvious):
x = 10
x = x + 1  # Add 1 to x

# GOOD comment (explains the purpose):
retry_count = 0
retry_count = retry_count + 1  # Increment to track failed login attempts

# Comments can go at the end of lines
TAX_RATE = 0.08  # California sales tax as of 2024
MAX_ATTEMPTS = 3  # Security policy: lock after 3 failed attempts

# Use comments to explain complex calculations
# Convert Celsius to Fahrenheit using the formula: F = C * 9/5 + 32
celsius = 25
fahrenheit = celsius * 9/5 + 32  # Result will be 77.0

# Comments for debugging (temporary)
print(f"Temperature: {fahrenheit}")  # TODO: Remove after testing
# print(f"Debug: celsius = {celsius}")  # Commented out debug line
