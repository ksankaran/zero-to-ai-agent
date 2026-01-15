# From: Zero to AI Agent, Chapter 5, Section 5.7
# File: exercise_2_5_7_solution.py

# validators.py module
"""Data validation utilities module"""

import re

class ValidationResult:
    """Class to store validation results"""
    def __init__(self, is_valid, message=""):
        self.is_valid = is_valid
        self.message = message
    
    def __str__(self):
        status = "✅ Valid" if self.is_valid else "❌ Invalid"
        return f"{status}: {self.message}"

def validate_email(email):
    """Check if email format is valid"""
    # Basic email pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not email:
        return ValidationResult(False, "Email cannot be empty")
    
    if re.match(pattern, email):
        return ValidationResult(True, "Email format is valid")
    else:
        return ValidationResult(False, "Invalid email format")

def validate_phone(phone):
    """Check if phone number is valid (10 digits)"""
    # Remove common formatting characters
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    if not cleaned:
        return ValidationResult(False, "Phone number cannot be empty")
    
    if len(cleaned) == 10 and cleaned.isdigit():
        return ValidationResult(True, "Valid 10-digit phone number")
    elif len(cleaned) == 11 and cleaned.startswith('1') and cleaned[1:].isdigit():
        return ValidationResult(True, "Valid 11-digit phone number (with country code)")
    else:
        return ValidationResult(False, f"Phone must be 10 digits, got {len(cleaned)}")

def validate_password(password):
    """Check password strength"""
    messages = []
    
    if len(password) < 8:
        messages.append("at least 8 characters")
    
    if not any(c.isupper() for c in password):
        messages.append("an uppercase letter")
    
    if not any(c.islower() for c in password):
        messages.append("a lowercase letter")
    
    if not any(c.isdigit() for c in password):
        messages.append("a number")
    
    if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
        messages.append("a special character")
    
    if messages:
        return ValidationResult(False, f"Password needs: {', '.join(messages)}")
    else:
        return ValidationResult(True, "Strong password!")

def validate_username(username):
    """Validate username (alphanumeric, 4-15 chars)"""
    if not username:
        return ValidationResult(False, "Username cannot be empty")
    
    if len(username) < 4:
        return ValidationResult(False, "Username must be at least 4 characters")
    
    if len(username) > 15:
        return ValidationResult(False, "Username must be 15 characters or less")
    
    if not username.isalnum():
        return ValidationResult(False, "Username must contain only letters and numbers")
    
    return ValidationResult(True, "Valid username")

# Test the module
if __name__ == "__main__":
    # Test email validation
    print("=== Email Validation ===")
    test_emails = [
        "valid@email.com",
        "also.valid+tag@company.co.uk",
        "invalid.email",
        "@invalid.com",
        ""
    ]
    for email in test_emails:
        result = validate_email(email)
        print(f"{email:30} -> {result}")
    
    # Test phone validation
    print("\n=== Phone Validation ===")
    test_phones = [
        "1234567890",
        "(123) 456-7890",
        "123-456-7890",
        "11234567890",
        "12345"
    ]
    for phone in test_phones:
        result = validate_phone(phone)
        print(f"{phone:20} -> {result}")
    
    # Test password validation
    print("\n=== Password Validation ===")
    test_passwords = [
        "weak",
        "12345678",
        "StrongPass123!",
        "NoNumbers!",
        "nouppercas3!"
    ]
    for password in test_passwords:
        result = validate_password(password)
        print(f"{password:20} -> {result}")
    
    # Test username validation
    print("\n=== Username Validation ===")
    test_usernames = [
        "john123",
        "abc",
        "verylongusernamethatexceedslimit",
        "user@name",
        "ValidUser99"
    ]
    for username in test_usernames:
        result = validate_username(username)
        print(f"{username:35} -> {result}")
