# From: Zero to AI Agent, Chapter 5, Section 5.6
# File: password_generator.py

import random
import string
from datetime import datetime

def generate_password(length=12, include_symbols=True):
    """Generate a secure random password"""
    
    # Define character sets
    lowercase = string.ascii_lowercase  # a-z
    uppercase = string.ascii_uppercase  # A-Z
    digits = string.digits              # 0-9
    symbols = string.punctuation        # !@#$%^&*() etc.
    
    # Build character pool
    char_pool = lowercase + uppercase + digits
    if include_symbols:
        char_pool += symbols
    
    # Ensure at least one of each type
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits)
    ]
    
    if include_symbols:
        password.append(random.choice(symbols))
    
    # Fill the rest randomly
    for _ in range(length - len(password)):
        password.append(random.choice(char_pool))
    
    # Shuffle to avoid predictable pattern
    random.shuffle(password)
    
    return ''.join(password)

def save_password(website, password):
    """Save password with timestamp (NOT for real use - just demo!)"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("passwords.txt", "a") as f:
        f.write(f"{timestamp} | {website} | {password}\n")
    
    print(f"Password saved for {website}")

# Generate some passwords
print("Password Generator v1.0")
print("-" * 40)

for site in ["email", "banking", "social"]:
    pwd = generate_password(16, include_symbols=True)
    print(f"{site:10} : {pwd}")
    save_password(site, pwd)

print("-" * 40)
print("⚠️  Remember: This is just for learning!")
print("Use a real password manager for actual passwords!")