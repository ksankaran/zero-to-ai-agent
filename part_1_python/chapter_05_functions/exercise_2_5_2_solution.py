# From: Zero to AI Agent, Chapter 5, Section 5.2
# File: exercise_2_5_2_solution.py

def check_password(password, min_length=8, require_numbers=True):
    """Check if a password is strong"""
    print(f"Checking password: {'*' * len(password)}")
    print(f"Requirements: min length={min_length}, numbers={'required' if require_numbers else 'optional'}")
    
    # Track what's wrong
    issues = []
    
    # Check length
    if len(password) < min_length:
        issues.append(f"Too short (needs {min_length} characters, has {len(password)})")
    
    # Check for numbers if required
    if require_numbers:
        has_number = any(char.isdigit() for char in password)
        if not has_number:
            issues.append("Missing numbers")
    
    # Report results
    if issues:
        print("❌ WEAK PASSWORD")
        for issue in issues:
            print(f"  - {issue}")
        print("Suggestion: Make it longer and add numbers!")
    else:
        print("✅ STRONG PASSWORD")
        print("Good job! Your password meets all requirements.")
    
    return len(issues) == 0  # Return True if strong, False if weak

# Test different passwords
check_password("hello")                          # Too short, no numbers
check_password("hellothere")                     # Long enough, but no numbers
check_password("hello123")                       # Perfect!
check_password("longpasswordnonum", require_numbers=False)  # Disable number requirement
check_password("short1", min_length=5)          # Lower the length requirement
