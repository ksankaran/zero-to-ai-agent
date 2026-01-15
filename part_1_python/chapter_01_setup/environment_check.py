# environment_check.py
# From: Zero to AI Agent, Chapter 1, Section 1.5

import sys
import os

print("=" * 50)
print("DEVELOPMENT ENVIRONMENT CHECK")
print("=" * 50)

# Check Python version
python_version = sys.version.split()[0]
print(f"Python Version: {python_version}")
print("")

# Check virtual environment
print(f"sys.prefix: {sys.prefix}")
print(f"sys.base_prefix: {sys.base_prefix}")
print("")

# Check current directory
current_dir = os.getcwd()
print(f"Current Directory: {current_dir}")
print("")

print("=" * 50)
print("CHECKLIST:")
print("=" * 50)
print("[ ] Python version shows 3.13.x")
print("[ ] sys.prefix contains 'venv' (virtual env active)")
print("[ ] You're in your project directory")
print("")
print("If all items check out, you're ready!")
print("=" * 50)
