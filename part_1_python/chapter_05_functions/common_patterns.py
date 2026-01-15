# From: Zero to AI Agent, Chapter 5, Section 5.2
# File: common_patterns.py

# Pattern 1: Configuration functions
def setup_game(difficulty="medium", sound=True, fullscreen=False):
    """Common pattern for configuration"""
    settings = {
        "difficulty": difficulty,
        "sound": sound,
        "fullscreen": fullscreen
    }
    print(f"Game settings: {settings}")
    return settings

# Pattern 2: Processing with options
def process_text(text, uppercase=False, remove_spaces=False):
    """Common pattern for text processing"""
    result = text
    if uppercase:
        result = result.upper()
    if remove_spaces:
        result = result.replace(" ", "")
    return result

# Pattern 3: Validation functions
def validate_age(age, minimum=0, maximum=120):
    """Common pattern for validation"""
    if age < minimum:
        print(f"Age {age} is too low (minimum: {minimum})")
        return False
    elif age > maximum:
        print(f"Age {age} is too high (maximum: {maximum})")
        return False
    else:
        print(f"Age {age} is valid!")
        return True

# Test our patterns
setup_game(difficulty="hard")
print(process_text("Hello World", uppercase=True))
validate_age(25, minimum=18, maximum=65)
