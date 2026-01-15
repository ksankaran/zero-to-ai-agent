# From: Zero to AI Agent, Chapter 6, Section 6.5
# File: 01_what_are_env_vars.py


import os
import sys

print("🌍 UNDERSTANDING ENVIRONMENT VARIABLES\n")

# Environment variables are already all around you!
print("="*50)
print("SYSTEM ENVIRONMENT VARIABLES YOU ALREADY HAVE:")
print("="*50)

# Common environment variables
common_vars = ['PATH', 'HOME', 'USER', 'SHELL', 'PWD']

for var in common_vars:
    value = os.environ.get(var)
    if value:
        # Show just first 50 chars for long values
        display_value = value[:50] + "..." if len(value) > 50 else value
        print(f"{var}: {display_value}")

# Your Python is using environment variables right now!
print("\n" + "="*50)
print("PYTHON-RELATED ENVIRONMENT VARIABLES:")
print("="*50)

print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version.split()[0]}")
print(f"Python path: {os.environ.get('PYTHONPATH', 'Not set')}")

# Count total environment variables
total_vars = len(os.environ)
print(f"\nTotal environment variables on your system: {total_vars}")

# Why use environment variables?
print("\n" + "="*50)
print("WHY ENVIRONMENT VARIABLES?")
print("="*50)

print("""
1. SECURITY: Keep secrets out of code
2. FLEXIBILITY: Different settings per environment
3. PORTABILITY: Same code works everywhere
4. SIMPLICITY: Change settings without changing code
5. STANDARD: Industry best practice
""")

# The WRONG way vs RIGHT way
print("="*50)
print("WRONG WAY vs RIGHT WAY:")
print("="*50)

print("❌ WRONG (Never do this!):")
print('api_key = "sk-1234567890abcdef"  # Visible in code!')

print("\n✅ RIGHT (Always do this!):")
print('api_key = os.environ.get("API_KEY")  # Secure!')
