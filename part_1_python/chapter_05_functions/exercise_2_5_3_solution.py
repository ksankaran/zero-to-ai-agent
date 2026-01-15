# From: Zero to AI Agent, Chapter 5, Section 5.3
# File: exercise_2_5_3_solution.py

def generate_username(first_name, last_name, birth_year):
    """Generate a username from personal information"""
    # Get first initial
    first_initial = first_name[0] if first_name else ""
    
    # Get last two digits of birth year
    year_suffix = str(birth_year)[-2:]
    
    # Combine and return lowercase
    username = (first_initial + last_name + year_suffix).lower()
    return username

def validate_username(username):
    """Check if username meets requirements"""
    # Check length
    if len(username) < 4 or len(username) > 15:
        return False
    
    # Check if it contains only alphanumeric characters
    if not username.isalnum():
        return False
    
    return True

def create_and_validate_username(first, last, year):
    """Helper function that creates and validates username"""
    username = generate_username(first, last, year)
    is_valid = validate_username(username)
    
    return username, is_valid

# Test the functions
username1 = generate_username("Alice", "Smith", 1995)
print(f"Generated username: {username1}")  # asmith95
print(f"Is valid? {validate_username(username1)}")  # True

username2 = generate_username("Bob", "Jo", 2001)
print(f"Generated username: {username2}")  # bjo01
print(f"Is valid? {validate_username(username2)}")  # False (too short)

# Test the combined function
user, valid = create_and_validate_username("Charlie", "Brown", 1999)
print(f"\nUsername: {user}, Valid: {valid}")