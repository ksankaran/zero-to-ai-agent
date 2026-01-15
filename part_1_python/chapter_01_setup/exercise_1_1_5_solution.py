# Save as: exercise_1_1_5_solution.py
"""
Exercise 1.5.1 Solution: Personalized Greeter

This program asks for the user's name and age,
calculates their birth year, and gives a personalized message.
"""

import datetime


def main():
    """Main function for the personalized greeter."""
    
    print("=" * 50)
    print("🎉 PERSONALIZED GREETER")
    print("=" * 50)
    
    # Get user's name
    name = input("\nWhat's your name? ").strip()
    
    # Get user's age (with error handling)
    while True:
        try:
            age = int(input(f"Nice to meet you, {name}! How old are you? "))
            if age < 0 or age > 150:
                print("Please enter a realistic age!")
                continue
            break
        except ValueError:
            print("Please enter a valid number!")
    
    # Calculate birth year
    current_year = datetime.datetime.now().year
    birth_year = current_year - age
    
    # Generate personalized message based on age
    print("\n" + "-" * 50)
    print(f"👋 Hello, {name}!")
    print(f"📅 You were born around {birth_year}")
    
    # Add age-specific message
    if age < 13:
        message = "You're starting young - that's amazing! 🌟"
    elif age < 20:
        message = "Learning to code as a teenager is perfect timing! 🚀"
    elif age < 30:
        message = "Your 20s are a great time to dive into programming! 💪"
    elif age < 40:
        message = "It's never too late to start coding - you've got this! 🎯"
    elif age < 50:
        message = "Your life experience will help you think like a programmer! 🧠"
    else:
        message = "Proof that learning has no age limit! You're inspiring! ✨"
    
    print(f"\n💬 {message}")
    
    # Fun fact based on birth year
    print(f"\n🔍 Fun fact: In {birth_year}...")
    
    if birth_year >= 2020:
        print("   The COVID-19 pandemic was changing the world.")
    elif birth_year >= 2010:
        print("   Smartphones were becoming essential to daily life.")
    elif birth_year >= 2000:
        print("   The internet boom was transforming everything.")
    elif birth_year >= 1990:
        print("   The World Wide Web was just getting started.")
    elif birth_year >= 1980:
        print("   Personal computers were becoming household items.")
    elif birth_year >= 1970:
        print("   The first video games were being invented.")
    else:
        print("   Computing was still in its early days!")
    
    # Calculate days until next birthday
    today = datetime.datetime.now()
    this_year_birthday = datetime.datetime(today.year, today.month, today.day)
    
    # Rough estimate - assuming birthday hasn't passed
    days_alive = age * 365
    print(f"\n📊 You've been alive approximately {days_alive:,} days!")
    
    print("\n" + "=" * 50)
    print(f"Thanks for sharing, {name}! Happy coding! 🐍")
    print("=" * 50)


if __name__ == "__main__":
    main()
