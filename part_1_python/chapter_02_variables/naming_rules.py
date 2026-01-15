# naming_rules.py
# From: Zero to AI Agent, Chapter 2, Section 2.1

# GOOD - These will work:
user_age = 30
userName = "Alice"
user_name_2 = "Bob"
_private_variable = "secret"

print("All valid variable names created successfully!")
print(f"user_age = {user_age}")
print(f"userName = {userName}")
print(f"user_name_2 = {user_name_2}")
print(f"_private_variable = {_private_variable}")

# BAD - These would cause errors (uncomment to test):
# 2nd_user = "Charlie"      # Can't start with a number
# user-name = "David"       # Can't use hyphens
# user name = "Eve"         # Can't have spaces
# class = "Python101"       # Can't use Python keywords
