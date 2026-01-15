# From: Zero to AI Agent, Chapter 6, Section 6.3
# Exercise 1 Solution: Weather Checker

"""
Weather Checker
Create a simple weather app using a free API.
"""

import requests

def get_weather(city):
    """Get weather for a city using wttr.in API"""
    try:
        # Build URL - wttr.in is free and needs no key!
        url = f"https://wttr.in/{city}?format=j1"
        
        # Make request
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract weather info
            current = data['current_condition'][0]
            temp_c = current['temp_C']
            desc = current['weatherDesc'][0]['value']
            humidity = current['humidity']
            
            # Display weather
            print(f"\n☀️ Weather in {city}:")
            print(f"  Temperature: {temp_c}°C")
            print(f"  Condition: {desc}")
            print(f"  Humidity: {humidity}%")
        else:
            print(f"❌ Could not get weather for {city}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: Could not connect to weather service")
    except KeyError:
        print(f"❌ City '{city}' not found!")

def main():
    print("=== Weather Checker ===")
    
    while True:
        city = input("\nEnter city name (or 'quit'): ")
        
        if city.lower() == 'quit':
            break
            
        get_weather(city)
    
    print("Stay weather aware! ☂️")

if __name__ == "__main__":
    main()
