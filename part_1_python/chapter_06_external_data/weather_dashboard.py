# From: Zero to AI Agent, Chapter 6, Section 6.3
# File: 05_weather_dashboard.py


import requests
import json
from datetime import datetime

class WeatherDashboard:
    def __init__(self):
        # Using OpenWeatherMap's free tier
        # Get your free API key at: https://openweathermap.org/api
        self.api_key = "DEMO"  # Replace with your key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        # For demo, we'll use a service that doesn't need a key
        self.demo_url = "https://wttr.in"
    
    def get_weather_demo(self, city):
        """Get weather using demo API (no key needed)"""
        try:
            # wttr.in provides weather in JSON format
            url = f"{self.demo_url}/{city}?format=j1"
            response = requests.get(url)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Error fetching weather: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return None
    
    def display_weather(self, city):
        """Display weather for a city"""
        print(f"\n🌤️  Weather for {city}")
        print("="*50)
        
        data = self.get_weather_demo(city)
        if not data:
            return
        
        try:
            current = data['current_condition'][0]
            location = data['nearest_area'][0]
            
            # Location info
            city_name = location['areaName'][0]['value']
            country = location['country'][0]['value']
            
            # Current conditions
            temp_c = current['temp_C']
            temp_f = current['temp_F']
            feels_like_c = current['FeelsLikeC']
            description = current['weatherDesc'][0]['value']
            humidity = current['humidity']
            wind_speed = current['windspeedKmph']
            
            print(f"📍 Location: {city_name}, {country}")
            print(f"🌡️  Temperature: {temp_c}°C ({temp_f}°F)")
            print(f"🤔 Feels like: {feels_like_c}°C")
            print(f"☁️  Condition: {description}")
            print(f"💧 Humidity: {humidity}%")
            print(f"💨 Wind: {wind_speed} km/h")
            
            # Forecast
            print("\n📅 3-Day Forecast:")
            for day in data['weather'][:3]:
                date = day['date']
                max_temp = day['maxtempC']
                min_temp = day['mintempC']
                desc = day['hourly'][4]['weatherDesc'][0]['value']  # Midday weather
                print(f"  {date}: {min_temp}°C - {max_temp}°C, {desc}")
                
        except KeyError as e:
            print(f"⚠️  Couldn't parse weather data: {e}")
    
    def compare_weather(self, cities):
        """Compare weather across multiple cities"""
        print("\n🌍 WEATHER COMPARISON")
        print("="*50)
        
        weather_data = []
        for city in cities:
            data = self.get_weather_demo(city)
            if data:
                current = data['current_condition'][0]
                weather_data.append({
                    'city': city,
                    'temp': int(current['temp_C']),
                    'condition': current['weatherDesc'][0]['value'],
                    'humidity': int(current['humidity'])
                })
        
        if weather_data:
            # Sort by temperature
            weather_data.sort(key=lambda x: x['temp'], reverse=True)
            
            print(f"{'City':<15} {'Temp':<8} {'Humidity':<10} {'Condition'}")
            print("-"*50)
            for w in weather_data:
                print(f"{w['city']:<15} {w['temp']}°C     {w['humidity']}%        {w['condition'][:20]}")
            
            # Find extremes
            hottest = weather_data[0]
            coldest = weather_data[-1]
            print(f"\n🔥 Hottest: {hottest['city']} ({hottest['temp']}°C)")
            print(f"❄️  Coldest: {coldest['city']} ({coldest['temp']}°C)")

def main():
    dashboard = WeatherDashboard()
    
    while True:
        print("\n" + "="*50)
        print("🌤️  WEATHER DASHBOARD")
        print("="*50)
        print("1. Check weather for a city")
        print("2. Compare multiple cities")
        print("3. Check major cities worldwide")
        print("4. Exit")
        
        choice = input("\nYour choice: ")
        
        if choice == "1":
            city = input("Enter city name: ").strip()
            if city:
                dashboard.display_weather(city)
        
        elif choice == "2":
            cities_input = input("Enter cities (comma-separated): ")
            cities = [c.strip() for c in cities_input.split(",") if c.strip()]
            if cities:
                dashboard.compare_weather(cities)
        
        elif choice == "3":
            major_cities = ["London", "New York", "Tokyo", "Sydney", "Dubai"]
            dashboard.compare_weather(major_cities)
        
        elif choice == "4":
            print("\n☀️  Thanks for using Weather Dashboard!")
            break

if __name__ == "__main__":
    print("🌤️  Welcome to the Python Weather Dashboard!")
    print("This demonstrates real API usage with weather data")
    main()
