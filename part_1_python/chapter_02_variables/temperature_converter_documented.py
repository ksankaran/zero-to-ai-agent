#!/usr/bin/env python3
# temperature_converter_documented.py
"""
Temperature Converter Script

This script converts temperatures between Celsius and Fahrenheit.
It demonstrates proper documentation for beginner Python programs.

Usage: Run the script and follow the prompts
Author: Your Name
Date: March 2024
Version: 1.0
"""

# ============================================================================
# CONSTANTS
# ============================================================================

# Physical constants for temperature
ABSOLUTE_ZERO_C = -273.15  # Lowest possible temperature in Celsius
WATER_FREEZING_C = 0       # Water freezes at 0°C
WATER_BOILING_C = 100      # Water boils at 100°C (at sea level)

# ============================================================================
# USER INPUT
# ============================================================================

print("Temperature Converter")
print("=" * 40)

# Get temperature value from user
temp_string = input("Enter temperature: ")
temperature = float(temp_string)  # Convert input to number

# Get the scale (C or F)
scale = input("Enter C for Celsius or F for Fahrenheit: ").upper()

# ============================================================================
# CONVERSION LOGIC
# ============================================================================

# Perform appropriate conversion based on input scale

# Convert from Celsius to Fahrenheit
is_celsius = scale == "C"
fahrenheit = temperature * 9/5 + 32

# Convert from Fahrenheit to Celsius  
is_fahrenheit = scale == "F"
celsius = (temperature - 32) * 5/9

# ============================================================================
# OUTPUT
# ============================================================================

# Display the result
print("\n" + "="*40)
print("RESULT")
print("="*40)

if is_celsius:
    print(f"Celsius: {temperature:.1f}°C")
    print(f"Fahrenheit: {fahrenheit:.1f}°F")
elif is_fahrenheit:
    print(f"Fahrenheit: {temperature:.1f}°F")
    print(f"Celsius: {celsius:.1f}°C")
else:
    print("Invalid scale entered. Please use C or F.")
