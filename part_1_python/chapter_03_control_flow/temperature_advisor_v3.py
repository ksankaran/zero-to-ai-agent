# From: Zero to AI Agent, Chapter 3, Section 3.1
# temperature_advisor_v3.py

temperature = float(input("What's the temperature in Celsius? "))

if temperature < 0:
    print("🥶 Freezing! Water will turn to ice!")
    print("Suggested: Heavy winter coat, gloves, and hat")
elif temperature < 10:
    print("🧥 Cold! Better wear a jacket.")
    print("Suggested: Light jacket or sweater")
elif temperature < 20:
    print("😊 Cool and comfortable!")
    print("Suggested: Long sleeves or light sweater")
elif temperature < 30:
    print("☀️ Warm and pleasant!")
    print("Suggested: T-shirt weather")
else:
    print("🔥 Hot! Stay hydrated!")
    print("Suggested: Light clothing and sunscreen")

print(f"\nYour temperature: {temperature}°C")
