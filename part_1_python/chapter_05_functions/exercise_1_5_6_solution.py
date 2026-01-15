# From: Zero to AI Agent, Chapter 5, Section 5.6
# File: exercise_1_5_6_solution.py

from datetime import datetime, date, timedelta

def calculate_age_details():
    """Calculate detailed age information"""
    
    # Get birthdate from user
    print("Enter your birthdate")
    year = int(input("Year (YYYY): "))
    month = int(input("Month (1-12): "))
    day = int(input("Day (1-31): "))
    
    # Create date objects
    birthdate = date(year, month, day)
    today = date.today()
    
    # Calculate age in different units
    age_days = (today - birthdate).days
    age_years = age_days // 365
    age_months = (age_days % 365) // 30
    remaining_days = (age_days % 365) % 30
    
    print(f"\n📅 Age Calculator Results 📅")
    print(f"{'='*40}")
    print(f"Birthdate: {birthdate.strftime('%B %d, %Y')}")
    print(f"Today: {today.strftime('%B %d, %Y')}")
    print(f"\nYour age:")
    print(f"  {age_years} years, {age_months} months, {remaining_days} days")
    print(f"  Total days lived: {age_days:,}")
    
    # Calculate next birthday
    this_year_birthday = date(today.year, month, day)
    if this_year_birthday < today:
        next_birthday = date(today.year + 1, month, day)
    else:
        next_birthday = this_year_birthday
    
    days_until = (next_birthday - today).days
    
    print(f"\nNext birthday: {next_birthday.strftime('%B %d, %Y')}")
    print(f"Days until birthday: {days_until}")
    
    if days_until == 0:
        print("🎉 Happy Birthday! 🎉")
    elif days_until <= 7:
        print("🎂 Your birthday is coming soon!")
    
    print(f"{'='*40}")

# Run the calculator
calculate_age_details()