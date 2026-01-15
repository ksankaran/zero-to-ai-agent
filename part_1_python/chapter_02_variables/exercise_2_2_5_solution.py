# Exercise 2: Unit Converter
# Convert between different units using type conversion

# Solution:

print("=" * 40)
print("UNIT CONVERTER")
print("=" * 40)

# Input values as strings (simulating user input)
miles_str = "26.2"
pounds_str = "150"
fahrenheit_str = "98.6"

# Convert strings to numbers
miles = float(miles_str)
pounds = float(pounds_str)
fahrenheit = float(fahrenheit_str)

print("\nOriginal values (as strings):")
print(f"  Miles: '{miles_str}'")
print(f"  Pounds: '{pounds_str}'")
print(f"  Fahrenheit: '{fahrenheit_str}'")

# Perform conversions
kilometers = miles * 1.60934
kilograms = pounds * 0.453592
celsius = (fahrenheit - 32) * 5/9

print("\nConverted values:")
print(f"  {miles} miles = {kilometers:.2f} kilometers")
print(f"  {pounds} pounds = {kilograms:.2f} kilograms")
print(f"  {fahrenheit}°F = {celsius:.1f}°C")

# Show the type changes
print("\nType conversions:")
print(f"  '{miles_str}' (str) -> {miles} (float)")
print(f"  '{pounds_str}' (str) -> {pounds} (float)")

print("=" * 40)
