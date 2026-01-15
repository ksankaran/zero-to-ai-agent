# From: Zero to AI Agent, Chapter 8, Section 8.1
# File: setup_api_key.py

import os
from pathlib import Path

def setup_api_key():
    """Set up your OpenAI API key safely"""
    
    print("🔐 Let's set up your OpenAI API key!")
    print("=" * 50)
    
    # Check if we already have a key saved
    env_file = Path(".env")
    if env_file.exists():
        print("✅ You already have a .env file!")
        with open(env_file, 'r') as f:
            if 'OPENAI_API_KEY' in f.read():
                print("✅ Your API key is already set up!")
                return
    
    # Get the API key from user
    print("\nYou need your OpenAI API key from: https://platform.openai.com/api-keys")
    print("(It starts with 'sk-')")
    print()
    
    api_key = input("Paste your API key here: ").strip()
    
    # Basic validation
    if not api_key.startswith('sk-'):
        print("⚠️  That doesn't look like an OpenAI key (should start with 'sk-')")
        print("But let's save it anyway - you can fix it later!")
    
    # Save to .env file
    with open('.env', 'w') as f:
        f.write(f"OPENAI_API_KEY={api_key}\n")
    
    print("\n✅ API key saved to .env file!")
    print("🔒 Remember: NEVER share this file or commit it to Git!")
    
    # Create .gitignore to keep it safe
    with open('.gitignore', 'w') as f:
        f.write(".env\n")
    
    print("✅ Created .gitignore to keep your key safe!")
    print("\n🎉 You're all set! Let's talk to AI!")

if __name__ == "__main__":
    setup_api_key()
