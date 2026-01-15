# boolean_basics.py
# From: Zero to AI Agent, Chapter 2, Section 2.4
# Understanding True and False in Python

# Creating boolean variables
is_raining = True
is_sunny = False
has_umbrella = True
wants_to_go_outside = True

print("Weather status:")
print(f"Is it raining? {is_raining}")
print(f"Is it sunny? {is_sunny}")
print(f"Do I have an umbrella? {has_umbrella}")
print(f"Do I want to go out? {wants_to_go_outside}")

# Booleans from comparisons
age = 25
is_adult = age >= 18
can_rent_car = age >= 25
gets_senior_discount = age >= 65

print(f"\nAge-based permissions for age {age}:")
print(f"Is adult? {is_adult}")
print(f"Can rent a car? {can_rent_car}")
print(f"Gets senior discount? {gets_senior_discount}")

# Check the type
print(f"\nType of True: {type(True)}")
print(f"Type of is_adult: {type(is_adult)}")
