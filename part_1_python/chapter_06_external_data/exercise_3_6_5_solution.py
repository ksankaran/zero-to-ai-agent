# From: Zero to AI Agent, Chapter 6, Section 6.5
# Exercise 3 Solution: Safe API Key Loader

"""
Safe API Key Loader
Create a program that safely loads and uses an API key.
"""

import os
from dotenv import load_dotenv

def create_env_example():
    """Create .env.example file"""
    with open('.env.example', 'w') as f:
        f.write("# Example environment file\n")
        f.write("# Copy this to .env and add your real values\n\n")
        f.write("API_KEY=your-api-key-here\n")
        f.write("API_URL=https://api.example.com\n")
    print("✅ Created .env.example file")

def load_api_key():
    """Safely load API key"""
    # Load from .env file
    load_dotenv()
    
    # Get API key
    api_key = os.environ.get('API_KEY', '')
    
    # Check if key exists
    if not api_key or api_key == 'your-api-key-here':
        print("⚠️ WARNING: No valid API key found!")
        print("Please add your API key to .env file")
        print("See .env.example for the format")
        return None
    
    return api_key

def use_api_key(api_key):
    """Demonstrate safe API key usage"""
    if not api_key:
        print("\n❌ Cannot proceed without API key")
        return
    
    # Show key is loaded (but hidden)
    masked = api_key[:4] + '****' if len(api_key) > 4 else '****'
    print(f"\n✅ API Key loaded: {masked}")
    
    # Simulate API usage
    print("\n🔌 Ready to make API calls!")
    print("(In real app, would use key for authentication)")

def main():
    print("=== Safe API Key Loader ===")
    
    # Create example file
    create_env_example()
    
    # Create .env if doesn't exist
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("API_KEY=demo-key-12345\n")
        print("✅ Created .env with demo key")
    
    # Load and use key
    api_key = load_api_key()
    use_api_key(api_key)
    
    print("\n🔒 Remember: Never commit .env to git!")
    print("Always use .gitignore to exclude it")

if __name__ == "__main__":
    main()
