# From: Zero to AI Agent, Chapter 6, Section 6.5
# Exercise 1 Solution: Simple Config Reader

"""
Simple Config Reader
Create a program that reads configuration from environment variables.
"""

import os
from dotenv import load_dotenv

def setup_env_file():
    """Create a sample .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("APP_NAME=My Cool App\n")
            f.write("DEBUG_MODE=True\n")
            f.write("API_KEY=sk-1234567890abcdef\n")
        print("✅ Created sample .env file")

def load_config():
    """Load configuration from environment"""
    # Load .env file
    load_dotenv()
    
    # Read configuration with defaults
    config = {
        'app_name': os.environ.get('APP_NAME', 'Default App'),
        'debug': os.environ.get('DEBUG_MODE', 'False'),
        'api_key': os.environ.get('API_KEY', '')
    }
    
    return config

def display_config(config):
    """Display configuration (hiding sensitive data)"""
    print("\n⚙️ Configuration:")
    print(f"  App Name: {config['app_name']}")
    print(f"  Debug Mode: {config['debug']}")
    
    # Hide API key - only show first 4 characters
    if config['api_key']:
        masked_key = config['api_key'][:4] + '****' if len(config['api_key']) > 4 else '****'
        print(f"  API Key: {masked_key}")
    else:
        print("  API Key: Not set")

def main():
    print("=== Simple Config Reader ===")
    
    # Setup sample .env if needed
    setup_env_file()
    
    # Load and display config
    config = load_config()
    display_config(config)
    
    print("\n💡 Tip: Edit .env file to change settings")
    print("Never commit .env files to git!")

if __name__ == "__main__":
    main()
