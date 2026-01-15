# Save as: exercise_2_1_5_solution.py
"""
Exercise 2 1.5 Solution: Temperature Converter

This program converts temperatures between Celsius and Fahrenheit.
Formula: F = C × 9/5 + 32
Reverse: C = (F - 32) × 5/9
"""


def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return celsius * 9/5 + 32


def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9


def get_temperature_description(celsius):
    """Get a description based on the temperature."""
    if celsius < -20:
        return "🥶 Extremely cold! Stay indoors!"
    elif celsius < 0:
        return "❄️ Freezing! Bundle up!"
    elif celsius < 10:
        return "🧥 Cold - wear a jacket!"
    elif celsius < 20:
        return "🍃 Cool and comfortable"
    elif celsius < 25:
        return "😊 Perfect weather!"
    elif celsius < 30:
        return "☀️ Warm and pleasant"
    elif celsius < 35:
        return "🌡️ Hot! Stay hydrated!"
    else:
        return "🔥 Extremely hot! Be careful!"


def main():
    """Main function for the temperature converter."""
    
    print("=" * 50)
    print("🌡️ TEMPERATURE CONVERTER")
    print("=" * 50)
    
    print("\nWhat would you like to convert?")
    print("  1. Celsius to Fahrenheit")
    print("  2. Fahrenheit to Celsius")
    print("  3. Convert both ways")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == "1":
        # Celsius to Fahrenheit
        try:
            celsius = float(input("\nEnter temperature in Celsius: "))
            fahrenheit = celsius_to_fahrenheit(celsius)
            
            print("\n" + "-" * 50)
            print(f"🌡️ {celsius:.1f}°C = {fahrenheit:.1f}°F")
            print(get_temperature_description(celsius))
            
        except ValueError:
            print("❌ Please enter a valid number!")
            
    elif choice == "2":
        # Fahrenheit to Celsius
        try:
            fahrenheit = float(input("\nEnter temperature in Fahrenheit: "))
            celsius = fahrenheit_to_celsius(fahrenheit)
            
            print("\n" + "-" * 50)
            print(f"🌡️ {fahrenheit:.1f}°F = {celsius:.1f}°C")
            print(get_temperature_description(celsius))
            
        except ValueError:
            print("❌ Please enter a valid number!")
            
    elif choice == "3":
        # Both ways
        try:
            temp = float(input("\nEnter a temperature value: "))
            
            print("\n" + "-" * 50)
            print(f"If {temp} is in Celsius:")
            fahrenheit = celsius_to_fahrenheit(temp)
            print(f"   {temp:.1f}°C = {fahrenheit:.1f}°F")
            print(f"   {get_temperature_description(temp)}")
            
            print(f"\nIf {temp} is in Fahrenheit:")
            celsius = fahrenheit_to_celsius(temp)
            print(f"   {temp:.1f}°F = {celsius:.1f}°C")
            print(f"   {get_temperature_description(celsius)}")
            
        except ValueError:
            print("❌ Please enter a valid number!")
    else:
        print("❌ Invalid choice! Please enter 1, 2, or 3.")
        return
    
    # Bonus: Show a reference table
    print("\n" + "=" * 50)
    print("📊 QUICK REFERENCE TABLE")
    print("=" * 50)
    print(f"{'Celsius':^15} {'Fahrenheit':^15}")
    print("-" * 30)
    
    reference_temps = [-40, -20, 0, 10, 20, 25, 30, 37, 100]
    for c in reference_temps:
        f = celsius_to_fahrenheit(c)
        note = ""
        if c == 0:
            note = " (Water freezes)"
        elif c == 37:
            note = " (Body temp)"
        elif c == 100:
            note = " (Water boils)"
        elif c == -40:
            note = " (Same in both!)"
        print(f"{c:^15.0f} {f:^15.0f}{note}")
    
    print("=" * 50)


if __name__ == "__main__":
    main()
