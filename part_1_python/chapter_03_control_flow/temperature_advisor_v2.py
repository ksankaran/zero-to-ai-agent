# From: Zero to AI Agent, Chapter 3, Section 3.1
# temperature_advisor_v2.py

temperature = float(input("What's the temperature in Celsius? "))

if temperature < 0:
    print("🥶 Freezing! Water will turn to ice!")
    print("Bundle up in warm clothes!")
else:
    print("😊 Above freezing! Water stays liquid.")
    print("No ice to worry about!")

print("\nThanks for using the temperature advisor!")
