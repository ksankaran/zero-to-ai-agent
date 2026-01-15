# From: Zero to AI Agent, Chapter 3, Section 3.1
# smart_weather_advisor.py

temperature = float(input("What's the temperature in Celsius? "))
is_raining = input("Is it raining? (yes/no): ").lower()

if temperature < 20:
    print("It's cool outside.")
    if is_raining == "yes":
        print("☔ And it's raining! Take an umbrella and wear a raincoat.")
    else:
        print("🌤️ At least it's dry! A light jacket will do.")
else:
    print("It's warm outside.")
    if is_raining == "yes":
        print("🌧️ But it's raining! Consider a light rain jacket.")
    else:
        print("☀️ And it's dry! Perfect weather for a t-shirt!")
