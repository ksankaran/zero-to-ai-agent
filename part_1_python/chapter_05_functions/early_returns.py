# From: Zero to AI Agent, Chapter 5, Section 5.3
# File: early_returns.py

# Without early returns - nested and hard to read
def validate_password_messy(password):
    if len(password) >= 8:
        if any(c.isupper() for c in password):
            if any(c.isdigit() for c in password):
                return "Password is valid!"
            else:
                return "Password needs a number"
        else:
            return "Password needs an uppercase letter"
    else:
        return "Password too short"

# With early returns - much cleaner!
def validate_password_clean(password):
    if len(password) < 8:
        return "Password too short"
    
    if not any(c.isupper() for c in password):
        return "Password needs an uppercase letter"
    
    if not any(c.isdigit() for c in password):
        return "Password needs a number"
    
    return "Password is valid!"

# Both work the same way
print(validate_password_clean("Pass123Word"))  # Password is valid!
print(validate_password_clean("short"))        # Password too short