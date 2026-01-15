# common_mistakes.py
# From: Zero to AI Agent, Chapter 2, Section 2.1

# Mistake 1: Using undefined variables
# print(user_name)  # Error! We haven't created user_name yet
user_name = "Charlie"
print(user_name)    # Now it works

# Mistake 2: Typos in variable names
user_age = 25
# print(user_Age)  # Error! Python is case-sensitive. 'age' and 'Age' are different

# Mistake 3: Confusing = with ==
age = 30          # This assigns 30 to age
# age == 30       # This checks if age equals 30 (we'll use this later)

# Mistake 4: Forgetting quotes around text
name = "Alice"    # Correct - text needs quotes
# name = Alice    # Error! Python thinks Alice is a variable name

# Mistake 5: Trying to use keywords
# def = 10        # Error! 'def' is a Python keyword
defense = 10      # This works!
