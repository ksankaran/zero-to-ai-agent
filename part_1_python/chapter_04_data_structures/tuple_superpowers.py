# From: Zero to AI Agent, Chapter 4, Section 4.3
# tuple_superpowers.py - Why immutability is actually useful

# 1. SAFETY - Protecting important data
# Imagine these are critical system settings
SYSTEM_SETTINGS = ("production", "api.company.com", 443, True)
# No one can accidentally modify these!
# If someone tries: SYSTEM_SETTINGS[0] = "development"  # ERROR!

print(f"System settings are protected: {SYSTEM_SETTINGS}")

# 2. DICTIONARY KEYS - Only immutable objects can be dictionary keys
# This is useful for coordinate systems, caching, etc.
location_names = {
    (40.7128, -74.0060): "New York City",
    (51.5074, -0.1278): "London",
    (35.6762, 139.6503): "Tokyo"
}

coordinates = (40.7128, -74.0060)
print(f"Location at {coordinates}: {location_names[coordinates]}")

# You CAN'T use lists as dictionary keys
# city_data = {[40.7, -74.0]: "NYC"}  # This would cause an error!

# 3. MULTIPLE RETURN VALUES - Clean way to return multiple values
# Calculate rectangle properties
width = 10
height = 5
area = width * height
perimeter = 2 * (width + height)

# Store multiple results in a tuple
rectangle_info = (area, perimeter)
print(f"Rectangle info (area, perimeter): {rectangle_info}")

# Unpack when using
calc_area, calc_perimeter = rectangle_info
print(f"Area: {calc_area}, Perimeter: {calc_perimeter}")

# 4. MEMORY EFFICIENCY - Tuples use less memory than lists
import sys

my_list = [1, 2, 3, 4, 5]
my_tuple = (1, 2, 3, 4, 5)

print(f"List size: {sys.getsizeof(my_list)} bytes")
print(f"Tuple size: {sys.getsizeof(my_tuple)} bytes")
# Tuples are smaller!
