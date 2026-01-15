# From: Zero to AI Agent, Chapter 6, Section 6.5
# Exercise 2 Solution: Environment Switcher

"""
Environment Switcher
Build a program that works differently in dev vs production.
"""

import os

def get_environment():
    """Get current environment"""
    return os.environ.get('ENVIRONMENT', 'development')

def get_file_path(filename):
    """Get file path based on environment"""
    env = get_environment()
    
    if env == 'production':
        return f"prod/{filename}"
    else:
        return f"dev/{filename}"

def debug_print(message):
    """Print debug messages only in development"""
    if get_environment() == 'development':
        print(f"[DEBUG] {message}")

def main():
    print("=== Environment Switcher ===")
    
    # Show current environment
    env = get_environment()
    print(f"\n🌍 Current Environment: {env}")
    
    # Environment-specific behavior
    if env == 'production':
        print("Running in PRODUCTION mode")
        print("- Debug messages: OFF")
        print("- Using production files")
        print("- Errors are hidden")
    else:
        print("Running in DEVELOPMENT mode")
        print("- Debug messages: ON")
        print("- Using development files")
        print("- Detailed errors shown")
    
    # Example file paths
    log_file = get_file_path("app.log")
    data_file = get_file_path("data.json")
    
    print(f"\n📁 File Paths:")
    print(f"  Log file: {log_file}")
    print(f"  Data file: {data_file}")
    
    # Debug messages
    debug_print("This message only shows in development")
    debug_print("Useful for troubleshooting!")
    
    print("\n💡 Tip: Set ENVIRONMENT=production to switch modes")

if __name__ == "__main__":
    main()
