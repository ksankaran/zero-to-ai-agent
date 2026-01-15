# Exercise 1: Boolean Comparisons
# Create boolean variables from comparisons

# Solution:

# Store user data
age = 25
password_attempt = "secret123"
correct_password = "secret123"
temperature = 72

# Create boolean variables
is_adult = age >= 18
is_teen = age >= 13 and age <= 19
is_senior = age >= 65
password_match = password_attempt == correct_password
is_comfortable = temperature >= 68 and temperature <= 76

# Display results
print("Boolean Comparisons")
print("=" * 40)
print("Age:", age)
print("Is adult (>= 18):", is_adult)
print("Is teen (13-19):", is_teen)
print("Is senior (>= 65):", is_senior)
print("\nPassword Check:")
print("Password matches:", password_match)
print("\nTemperature:", temperature, "°F")
print("Is comfortable (68-76):", is_comfortable)

# Additional comparisons
print("\n--- More Comparisons ---")
print("Age is exactly 25:", age == 25)
print("Age is not 30:", age != 30)
print("Temperature is above freezing:", temperature > 32)
