# From: Zero to AI Agent, Chapter 5, Section 5.7
# File: professional_module.py

# file: professional_module.py
"""
Module Title: Professional Module Template
Author: Your Name
Date: November 2024
Description: This module demonstrates best practices.

Usage:
    import professional_module
    result = professional_module.main_function()
"""

# Imports grouped and ordered
import os
import sys
from datetime import datetime

# import external_library  # Third-party imports

# Constants (UPPERCASE)
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
API_VERSION = "1.0.0"

# Module-level variables (if needed)
_private_var = "This is private (starts with _)"
public_var = "This is public"

# Classes
class MyClass:
    """Document your classes"""
    pass

# Functions
def public_function(param1, param2=None):
    """
    Document your functions!
    
    Args:
        param1 (str): Description of param1
        param2 (int, optional): Description of param2
        
    Returns:
        dict: Description of return value
        
    Example:
        result = public_function("test", 42)
    """
    return {"param1": param1, "param2": param2}

def _private_function():
    """Functions starting with _ are considered private"""
    pass

# Main execution
if __name__ == "__main__":
    # This runs only when module is executed directly
    print(f"Module {__name__} running directly")
    # Test code here