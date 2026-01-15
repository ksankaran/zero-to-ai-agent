# From: Zero to AI Agent, Chapter 3, Section 3.2
# Exercise 2: Password Validator
# Check password strength with specific requirements

print("=" * 40)
print("PASSWORD STRENGTH VALIDATOR")
print("=" * 40)

username = input("Enter your username: ")
password = input("Enter your password: ")

# Track validation results
is_valid = True
error_count = 0

print("")
print("Checking password requirements...")
print("-" * 40)

# Check length
if len(password) < 8:
    is_valid = False
    error_count = error_count + 1
    print("[X] Password must be at least 8 characters long")
else:
    print("[OK] Password length is good")

# Check for common bad passwords
if password == "password" or password == "12345678":
    is_valid = False
    error_count = error_count + 1
    print("[X] Password is too common and easily guessed")

# Check if password equals username
if password == username:
    is_valid = False
    error_count = error_count + 1
    print("[X] Password cannot be the same as your username")

# Check if password is all numbers
if password.isdigit():
    is_valid = False
    error_count = error_count + 1
    print("[X] Password should not be all numbers")

# Check if password is all letters
if password.isalpha():
    is_valid = False
    error_count = error_count + 1
    print("[X] Password should not be all letters")
else:
    if not password.isdigit():
        print("[OK] Password has a mix of characters")

# Display final result
print("-" * 40)
if is_valid:
    print("Password is STRONG and accepted!")
    print(f"Length: {len(password)} characters")
else:
    print(f"Password validation FAILED ({error_count} issues)")
    print("")
    print("Tips for a strong password:")
    print("  - Use at least 8 characters")
    print("  - Mix letters and numbers")
    print("  - Avoid common passwords")

print("=" * 40)
