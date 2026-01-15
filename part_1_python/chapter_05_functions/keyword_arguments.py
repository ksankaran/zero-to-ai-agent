# From: Zero to AI Agent, Chapter 5, Section 5.2
# File: keyword_arguments.py

def create_user_profile(username, age, email, country="USA", premium=False):
    """Create a user profile with mixed parameters"""
    print("Creating user profile...")
    print(f"  Username: {username}")
    print(f"  Age: {age}")
    print(f"  Email: {email}")
    print(f"  Country: {country}")
    print(f"  Premium: {premium}")
    print("Profile created successfully!")
    print("-" * 40)

# Positional arguments (order matters)
create_user_profile("alice_wonder", 25, "alice@example.com")

# Keyword arguments (order doesn't matter!)
create_user_profile(
    email="bob@example.com",
    age=30,
    username="bob_builder"
)

# Mix positional and keyword (positional must come first)
create_user_profile("charlie", 28, 
                   email="charlie@example.com",
                   country="Canada", 
                   premium=True)

# Using keywords to skip defaults
create_user_profile("diana", 35, "diana@example.com", premium=True)
