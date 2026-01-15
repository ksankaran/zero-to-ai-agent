# From: Zero to AI Agent, Chapter 5, Section 5.6
# File: exercise_3_5_6_solution.py

import random
import statistics
import json
from datetime import datetime, timedelta

def generate_weather_data():
    """Generate and analyze weather data"""
    
    # Generate fake temperature data for 7 days
    random.seed(42)  # For reproducible results
    
    # Create realistic temperature patterns
    base_temp = random.uniform(15, 25)  # Base temperature
    temperatures = []
    dates = []
    
    today = datetime.now()
    
    for day in range(7):
        # Add some variation
        daily_variation = random.uniform(-5, 5)
        morning_temp = base_temp + daily_variation - 3
        afternoon_temp = base_temp + daily_variation + 5
        evening_temp = base_temp + daily_variation
        
        # Store the day's data
        date_str = (today + timedelta(days=day)).strftime("%Y-%m-%d")
        dates.append(date_str)
        
        day_temps = {
            "date": date_str,
            "morning": round(morning_temp, 1),
            "afternoon": round(afternoon_temp, 1),
            "evening": round(evening_temp, 1),
            "average": round((morning_temp + afternoon_temp + evening_temp) / 3, 1)
        }
        temperatures.append(day_temps)
    
    # Calculate statistics
    all_temps = []
    for day in temperatures:
        all_temps.extend([day["morning"], day["afternoon"], day["evening"]])
    
    stats = {
        "mean": round(statistics.mean(all_temps), 2),
        "median": round(statistics.median(all_temps), 2),
        "stdev": round(statistics.stdev(all_temps), 2),
        "min": round(min(all_temps), 2),
        "max": round(max(all_temps), 2)
    }
    
    # Display results
    print("\n🌡️ Weather Data Analysis 🌡️")
    print("=" * 50)
    print("7-Day Temperature Forecast (°C):")
    
    for day in temperatures:
        print(f"\n{day['date']}:")
        print(f"  Morning:   {day['morning']:5.1f}°C")
        print(f"  Afternoon: {day['afternoon']:5.1f}°C")
        print(f"  Evening:   {day['evening']:5.1f}°C")
        print(f"  Average:   {day['average']:5.1f}°C")
    
    print("\n" + "=" * 50)
    print("Statistical Summary:")
    print(f"  Mean:   {stats['mean']:.2f}°C")
    print(f"  Median: {stats['median']:.2f}°C")
    print(f"  StdDev: {stats['stdev']:.2f}°C")
    print(f"  Min:    {stats['min']:.2f}°C")
    print(f"  Max:    {stats['max']:.2f}°C")
    
    # Save to JSON file
    weather_data = {
        "generated_at": datetime.now().isoformat(),
        "daily_temperatures": temperatures,
        "statistics": stats
    }
    
    with open("weather_data.json", "w") as f:
        json.dump(weather_data, f, indent=2)
    
    print("\n✅ Data saved to weather_data.json")
    print("=" * 50)
    
    return temperatures, stats

# Generate and analyze the weather data
temps, stats = generate_weather_data()

# Bonus: Create a simple forecast
if stats["mean"] > 20:
    print("\n☀️ Forecast: Warm week ahead! Don't forget sunscreen!")
elif stats["mean"] > 15:
    print("\n⛅ Forecast: Mild temperatures expected. Perfect weather!")
else:
    print("\n🌥️ Forecast: Cool temperatures. Bring a light jacket!")