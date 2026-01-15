# my_first_program.py
# From: Zero to AI Agent, Chapter 1, Section 1.4

print("=" * 50)
print("MY PYTHON PACKAGE EXPLORER")
print("=" * 50)

# First, let's check if our packages work
print("\n📦 Testing installed packages:\n")

# Test requests
try:
    import requests
    print("✅ requests is installed and working!")
except ImportError:
    print("❌ requests is not installed")

# Test colorama (if you installed it)
try:
    import colorama
    print("✅ colorama is installed and working!")
except ImportError:
    print("❌ colorama is not installed")

# Test rich (if you installed it)
try:
    import rich
    print("✅ rich is installed and working!")
except ImportError:
    print("❌ rich is not installed")

print("\n" + "=" * 50)
print("To see all packages, run: pip list")
print("To see details, run: pip show [package_name]")
print("=" * 50)