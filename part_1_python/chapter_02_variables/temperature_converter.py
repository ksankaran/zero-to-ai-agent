# temperature_converter.py
# From: Zero to AI Agent, Chapter 2, Section 2.1
# A simple Celsius to Fahrenheit converter

# Store the temperature in Celsius
celsius_temp = 25

# Convert to Fahrenheit (formula: F = C * 9/5 + 32)
fahrenheit_temp = celsius_temp * 9/5 + 32

# Create a nice message
location = "San Francisco"
weather_report = "The temperature in"

# Display the results
print(weather_report, location)
print("Celsius:", celsius_temp)
print("Fahrenheit:", fahrenheit_temp)

# Let's check a different temperature
celsius_temp = 0  # Freezing point of water
fahrenheit_temp = celsius_temp * 9/5 + 32
print("\nFreezing point of water:")
print("Celsius:", celsius_temp)
print("Fahrenheit:", fahrenheit_temp)
