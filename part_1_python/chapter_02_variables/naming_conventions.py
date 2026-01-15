# naming_conventions.py
# From: Zero to AI Agent, Chapter 2, Section 2.1

# Snake Case (Python's favorite - use this most of the time)
user_age = 30
first_name = "John"
is_logged_in = True
calculate_total_price = 99.99

# Camel Case (sometimes used, but less common in Python)
userName = "Jane"
isLoggedIn = True

# SCREAMING_SNAKE_CASE (for constants - values that never change)
MAX_LOGIN_ATTEMPTS = 3
PI = 3.14159
COMPANY_NAME = "AI Agents Inc."

# Single letters (okay for quick math, avoid elsewhere)
x = 10  # Fine for math
y = 20  # Fine for math
n = "Nancy"  # Bad - what does 'n' mean? name? number? 

# Descriptive names (ALWAYS better than cryptic ones)
# Bad:
d = 30

# Good:
days_until_deadline = 30

# Bad:
calc = 2500

# Good:
monthly_salary_calculation = 2500

print("Naming conventions demonstrated!")
print(f"Snake case: user_age = {user_age}")
print(f"Constant: MAX_LOGIN_ATTEMPTS = {MAX_LOGIN_ATTEMPTS}")
print(f"Descriptive: days_until_deadline = {days_until_deadline}")
