# converting_to_strings.py
# From: Zero to AI Agent, Chapter 2, Section 2.5
# Converting other types to strings

# Numbers to strings
age = 25
price = 19.99
is_member = True

age_string = str(age)
price_string = str(price)
member_string = str(is_member)

print("=== Converting to Strings ===")
print(f"Original age: {age}, type: {type(age)}")
print(f"String age: {age_string}, type: {type(age_string)}")
print("Can now concatenate: " + age_string + " years old")

# Why convert to strings?
# Problem: Can't concatenate string and number directly
# This would error: message = "You are " + age + " years old"

# Solution 1: Convert to string first
message = "You are " + str(age) + " years old"
print(message)

# Solution 2: Use f-strings (automatic conversion!)
message = f"You are {age} years old"  # Python converts for you!
print(message)
