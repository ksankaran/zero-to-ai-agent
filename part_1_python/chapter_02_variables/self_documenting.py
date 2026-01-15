# self_documenting.py
# From: Zero to AI Agent, Chapter 2, Section 2.7
# Writing code that explains itself

# BAD: Cryptic variable names need comments
d = 86400  # seconds in a day
t = d * 7  # seconds in a week

# GOOD: Clear names eliminate need for comments
SECONDS_PER_DAY = 86400
seconds_per_week = SECONDS_PER_DAY * 7

# BAD: Magic numbers need explanation
temp = 98.7
is_fever = temp > 98.6  # What is 98.6?

# GOOD: Named constants are self-explanatory
NORMAL_BODY_TEMP_F = 98.6
temperature_fahrenheit = 98.7
has_fever = temperature_fahrenheit > NORMAL_BODY_TEMP_F

# BAD: Complex expression
age = 25
verified = True
banned = False
eligible = age >= 18 and age <= 65 and verified and not banned

# GOOD: Break into meaningful parts with descriptive names
is_adult = age >= 18
is_under_retirement = age <= 65
is_verified = verified
is_not_banned = not banned
is_eligible = is_adult and is_under_retirement and is_verified and is_not_banned

print("Self-documenting code examples:")
print(f"Seconds per week: {seconds_per_week}")
print(f"Has fever: {has_fever}")
print(f"Is eligible: {is_eligible}")
