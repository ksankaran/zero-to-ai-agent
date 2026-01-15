# From: Zero to AI Agent, Chapter 6, Section 6.5
# File: 03_dotenv_files.py


import os

print("📁 WORKING WITH .ENV FILES\n")

# First, let's create a sample .env file
print("="*50)
print("CREATING A .ENV FILE:")
print("="*50)

env_content = """# Development Environment Variables
# NEVER commit this file to Git!

# API Keys
OPENAI_API_KEY=sk-fake-key-for-demo
GITHUB_TOKEN=ghp_fake_token_for_demo

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp_dev
DB_USER=developer
DB_PASSWORD=dev_password_123

# Application Settings
APP_ENV=development
DEBUG=True
SECRET_KEY=my-super-secret-key-change-in-production
PORT=3000

# Feature Flags
ENABLE_CACHE=False
ENABLE_ANALYTICS=False
MAX_UPLOAD_SIZE=10485760
"""

# Save the .env file
with open('.env.example', 'w') as f:
    f.write(env_content)

print("✅ Created .env.example file")
print("\nContents:")
print(env_content)

# Simple function to load .env file (without python-dotenv)
def load_dotenv(filepath='.env'):
    """Simple .env file loader"""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Skip comments and empty lines
            if line.startswith('#') or not line:
                continue
            
            # Parse KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                
                os.environ[key] = value
    
    return True

print("\n" + "="*50)
print("LOADING .ENV FILE:")
print("="*50)

# Load our example file
if load_dotenv('.env.example'):
    print("✅ Loaded .env.example")
    
    # Now we can use the variables
    print(f"\nLoaded variables:")
    print(f"  APP_ENV: {os.environ.get('APP_ENV')}")
    print(f"  DEBUG: {os.environ.get('DEBUG')}")
    print(f"  PORT: {os.environ.get('PORT')}")
    print(f"  DB_HOST: {os.environ.get('DB_HOST')}")

# Using python-dotenv (the professional way)
print("\n" + "="*50)
print("USING PYTHON-DOTENV PACKAGE:")
print("="*50)

print("""
To use the professional python-dotenv package:

1. Install it:
   pip install python-dotenv

2. Use it in your code:
   from dotenv import load_dotenv
   load_dotenv()  # Loads .env file

3. Access variables normally:
   api_key = os.environ.get('API_KEY')
""")

# Best practices for .env files
print("\n" + "="*50)
print("🎯 .ENV FILE BEST PRACTICES:")
print("="*50)

print("""
1. NEVER commit .env to Git (add to .gitignore)
2. Create .env.example with dummy values
3. Document all required variables
4. Use descriptive variable names
5. Keep development and production separate
6. Don't put spaces around = sign
7. Use quotes for values with spaces
""")

# Create a .gitignore file
gitignore_content = """# Environment variables
.env
.env.local
.env.production

# But include the example
!.env.example

# Python
__pycache__/
*.pyc
.python-version

# IDE
.vscode/
.idea/
"""

with open('.gitignore', 'w') as f:
    f.write(gitignore_content)

print("\n✅ Created .gitignore file to protect your secrets!")
