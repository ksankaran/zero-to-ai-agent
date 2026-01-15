# From: Zero to AI Agent, Chapter 5, Section 5.3
# File: chaining_functions.py

def get_user_input():
    """Get a number from user"""
    return float(input("Enter a number: "))

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32

def fahrenheit_to_kelvin(fahrenheit):
    """Convert Fahrenheit to Kelvin"""
    return (fahrenheit + 459.67) * 5/9

def format_temperatures(c, f, k):
    """Format all three temperatures nicely"""
    return f"""
Temperature Conversions:
-----------------------
Celsius:    {c:.1f}°C
Fahrenheit: {f:.1f}°F
Kelvin:     {k:.1f}K
"""

# Chain them all together!
celsius = get_user_input()
fahrenheit = celsius_to_fahrenheit(celsius)
kelvin = fahrenheit_to_kelvin(fahrenheit)
output = format_temperatures(celsius, fahrenheit, kelvin)
print(output)