# From: Zero to AI Agent, Chapter 6, Section 6.4
# File: 03_exception_info.py


import sys

try:
    numbers = [1, 2, 3]
    value = numbers[10]
except IndexError as e:
    # Get exception details
    print(f"Type: {type(e).__name__}")
    print(f"Message: {str(e)}")
    print(f"Args: {e.args}")
    
    # Get traceback info
    exc_type, exc_value, exc_tb = sys.exc_info()
    print(f"Line number: {exc_tb.tb_lineno}")
    
    # Save for logging
    error_log = {
        'type': type(e).__name__,
        'message': str(e),
        'line': exc_tb.tb_lineno
    }
