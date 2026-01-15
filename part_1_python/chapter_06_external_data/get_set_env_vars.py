# From: Zero to AI Agent, Chapter 6, Section 6.5
# File: 02_get_set_env_vars.py


import os

print("🔧 WORKING WITH ENVIRONMENT VARIABLES\n")

# Method 1: Getting environment variables
print("="*50)
print("1. GETTING ENVIRONMENT VARIABLES:")
print("="*50)

# Basic get (might raise KeyError if not found)
# Uncomment to see error:
# api_key = os.environ['MISSING_KEY']  # KeyError!

# Safe get with default value
api_key = os.environ.get('MY_API_KEY', 'not-set')
print(f"API Key: {api_key}")

# Check if variable exists
if 'MY_API_KEY' in os.environ:
    print("✅ MY_API_KEY is set")
else:
    print("❌ MY_API_KEY is not set")

# Method 2: Setting environment variables (in Python)
print("\n" + "="*50)
print("2. SETTING ENVIRONMENT VARIABLES (in Python):")
print("="*50)

# Set a variable for this Python process
os.environ['MY_CUSTOM_VAR'] = 'Hello from Python!'
print(f"Set MY_CUSTOM_VAR to: {os.environ['MY_CUSTOM_VAR']}")

# Note: This only affects the current Python process and its children
print("⚠️  Note: This only affects current Python session")

# Method 3: Multiple ways to access
print("\n" + "="*50)
print("3. DIFFERENT ACCESS METHODS:")
print("="*50)

# Set a test variable
os.environ['TEST_VAR'] = 'test_value'

# Different ways to get it
print("Using os.environ['KEY']:")
try:
    value1 = os.environ['TEST_VAR']
    print(f"  ✅ Got: {value1}")
except KeyError:
    print("  ❌ Key not found")

print("\nUsing os.environ.get('KEY'):")
value2 = os.environ.get('TEST_VAR')
print(f"  ✅ Got: {value2}")

print("\nUsing os.getenv('KEY'):")
value3 = os.getenv('TEST_VAR')
print(f"  ✅ Got: {value3}")

print("\nWith default value:")
value4 = os.getenv('MISSING_VAR', 'default_value')
print(f"  ✅ Got: {value4}")

# Method 4: Working with different types
print("\n" + "="*50)
print("4. HANDLING DIFFERENT DATA TYPES:")
print("="*50)

# Environment variables are always strings!
os.environ['PORT'] = '8080'
os.environ['DEBUG'] = 'True'
os.environ['MAX_CONNECTIONS'] = '100'

# Convert to appropriate types
port = int(os.environ.get('PORT', 3000))
debug = os.environ.get('DEBUG', 'False').lower() == 'true'
max_conn = int(os.environ.get('MAX_CONNECTIONS', 50))

print(f"Port (int): {port}, Type: {type(port)}")
print(f"Debug (bool): {debug}, Type: {type(debug)}")
print(f"Max Connections (int): {max_conn}, Type: {type(max_conn)}")
