# multiline_comments.py
# From: Zero to AI Agent, Chapter 2, Section 2.7
# Different ways to write longer comments

# Method 1: Multiple single-line comments
# This is a longer explanation that needs multiple lines.
# Each line starts with a # symbol.
# This is the most common approach for block comments.

# Method 2: Triple-quoted strings (technically not comments)
"""
This is a multi-line string, not technically a comment.
Python doesn't ignore it - it creates a string object.
But if not assigned to anything, it effectively acts like a comment.
Use this for module/script documentation.
"""

# Section headers with comments
# ============================================================================
# CONFIGURATION SETTINGS
# ============================================================================

# Database settings
DB_HOST = "localhost"
DB_PORT = 5432

# ============================================================================
# CALCULATIONS
# ============================================================================

# Calculate compound interest
principal = 1000  # Starting amount in dollars
rate = 0.05      # 5% annual interest rate
time = 3         # Investment period in years
amount = principal * (1 + rate) ** time
print(f"${principal} invested at {rate*100}% for {time} years = ${amount:.2f}")
