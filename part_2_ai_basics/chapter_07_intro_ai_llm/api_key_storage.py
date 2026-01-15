# From: Zero to AI Agent, Chapter 7, Section 7.6
# File: api_key_storage.py

"""
Demonstrates the right and wrong ways to store API keys in your code.
Critical for security and preventing expensive mistakes.
"""

import os
from dotenv import load_dotenv


# ============================================================================
# ❌ NEVER DO THIS - EXAMPLES OF WHAT NOT TO DO
# ============================================================================

def bad_example_hardcoded():
    """
    NEVER hardcode API keys directly in your code!
    This is the #1 security mistake beginners make.
    """
    # ❌ NEVER DO THIS
    # api_key = "sk-proj-KJ5hLvP9Ym8NwZ3bT7BlbkFJ4Xq2RnD8sFgH6kLpMc1A"
    
    # Even if the repo is private, don't do this!
    # Keys can be exposed through:
    # - Accidentally making repo public
    # - Sharing code snippets
    # - Screenshots or demos
    # - Git history (even after deletion)
    
    print("❌ Example of what NOT to do - hardcoding keys")
    print("This would expose your key to anyone who sees the code")


def bad_example_in_comments():
    """Even in comments, never include real API keys!"""
    
    # ❌ NEVER DO THIS EITHER
    # My API key: sk-proj-KJ5hLvP9Ym8NwZ3bT7BlbkFJ4Xq2RnD8sFgH6kLpMc1A
    # TODO: Remove this before committing
    
    print("❌ Don't put keys in comments either - they often get forgotten")


# ============================================================================
# ✅ ALWAYS DO THIS - SECURE API KEY HANDLING
# ============================================================================

def good_example_environment_variable():
    """
    ✅ CORRECT: Load API keys from environment variables
    This keeps your keys separate from your code.
    """
    # Load from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("No API key found!")
        print("Please set it using:")
        print("  Mac/Linux: export OPENAI_API_KEY='your-key-here'")
        print("  Windows: set OPENAI_API_KEY=your-key-here")
        return None
    
    # Never print the actual key!
    print(f"✅ API key loaded successfully (starts with {api_key[:7]}...)")
    return api_key


def good_example_dotenv():
    """
    ✅ CORRECT: Load from .env file using python-dotenv
    This is convenient for development.
    """
    # Load .env file
    load_dotenv()
    
    # Now get the key
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("No API key found in .env file!")
        print("Create a .env file with:")
        print("  OPENAI_API_KEY=your-key-here")
        return None
    
    print("✅ API key loaded from .env file")
    return api_key


def good_example_with_validation():
    """
    ✅ BEST PRACTICE: Load with validation and error handling
    """
    # Try multiple sources
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        # Try loading from .env as fallback
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "API key not found!\n"
            "Please set OPENAI_API_KEY environment variable or add to .env file"
        )
    
    # Validate format (basic check)
    if not api_key.startswith("sk-"):
        print("⚠️ Warning: API key format might be incorrect")
    
    # Check for common mistakes
    if " " in api_key:
        raise ValueError("API key contains spaces - probably a copy/paste error")
    
    if len(api_key) < 20:
        raise ValueError("API key seems too short - might be truncated")
    
    print("✅ API key validated and ready to use")
    return api_key


# ============================================================================
# SETTING UP YOUR PROJECT CORRECTLY
# ============================================================================

def setup_project_security():
    """
    Set up a new project with proper security from the start
    """
    import os
    from pathlib import Path
    
    print("Setting up secure API key management...")
    
    # 1. Create .env file if it doesn't exist
    if not Path(".env").exists():
        with open(".env", "w") as f:
            f.write("# API Keys - NEVER commit this file!\n")
            f.write("OPENAI_API_KEY=your-key-here\n")
            f.write("ANTHROPIC_API_KEY=your-key-here\n")
            f.write("GOOGLE_API_KEY=your-key-here\n")
        print("✅ Created .env file")
    
    # 2. Create .env.example for others
    with open(".env.example", "w") as f:
        f.write("# Copy this to .env and add your actual keys\n")
        f.write("OPENAI_API_KEY=ADD_YOUR_KEY_HERE\n")
        f.write("ANTHROPIC_API_KEY=ADD_YOUR_KEY_HERE\n")
        f.write("GOOGLE_API_KEY=ADD_YOUR_KEY_HERE\n")
    print("✅ Created .env.example (safe to commit)")
    
    # 3. Create/update .gitignore
    gitignore_lines = [
        "# Environment variables",
        ".env",
        ".env.local",
        ".env.*.local",
        "",
        "# API keys and secrets",
        "config.json",
        "secrets.json",
        "*.key",
        "",
        "# Python",
        "__pycache__/",
        "*.py[cod]",
        "venv/",
        "env/",
    ]
    
    with open(".gitignore", "w") as f:
        f.write("\n".join(gitignore_lines))
    print("✅ Created .gitignore to protect secrets")
    
    print("\n✅ Project security setup complete!")
    print("Next steps:")
    print("1. Edit .env and add your actual API keys")
    print("2. Run: pip install python-dotenv")
    print("3. Use load_dotenv() in your code")


if __name__ == "__main__":
    print("=" * 60)
    print("API KEY SECURITY DEMONSTRATION")
    print("=" * 60)
    
    # Show what NOT to do
    print("\n⚠️ EXAMPLES OF BAD PRACTICES:")
    print("-" * 40)
    bad_example_hardcoded()
    
    print("\n✅ EXAMPLES OF GOOD PRACTICES:")
    print("-" * 40)
    
    # Try to load API key the right way
    try:
        key = good_example_with_validation()
        if key:
            print(f"Success! Key starts with: {key[:10]}...")
    except Exception as e:
        print(f"Setup needed: {e}")
    
    print("\n💡 TIP: Run setup_project_security() to set up your project correctly!")
