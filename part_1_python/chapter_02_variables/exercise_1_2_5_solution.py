# Exercise 1: Type Detective
# Determine types and convert values between int, float, bool, str

# Solution:

# Various values to check
value1 = 42
value2 = 3.14
value3 = "100"
value4 = True
value5 = "False"
value6 = ""

print("Type Detective")
print("=" * 40)

# Check types
print("Original Types:")
print(f"42 is type: {type(value1)}")
print(f"3.14 is type: {type(value2)}")
print(f'"100" is type: {type(value3)}')
print(f"True is type: {type(value4)}")
print(f'"False" is type: {type(value5)}')
print(f'"" (empty string) is type: {type(value6)}')

# Convert and display
print("\nConversions:")

# Convert 42 to other types
print("\n42 conversions:")
print(f"To float: {float(value1)} (type: {type(float(value1))})")
print(f"To string: {str(value1)} (type: {type(str(value1))})")
print(f"To bool: {bool(value1)} (type: {type(bool(value1))})")

# Convert "100" to other types
print('\n"100" conversions:')
print(f"To int: {int(value3)} (type: {type(int(value3))})")
print(f"To float: {float(value3)} (type: {type(float(value3))})")
print(f"To bool: {bool(value3)} (type: {type(bool(value3))})")

# Boolean conversions
print("\nBoolean conversions:")
print(f"bool(0): {bool(0)}")
print(f"bool(1): {bool(1)}")
print(f"bool(''): {bool('')}")
print(f"bool('text'): {bool('text')}")
print(f"bool(None): {bool(None)}")
