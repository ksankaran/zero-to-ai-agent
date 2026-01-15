# From: Zero to AI Agent, Chapter 5, Section 5.1
# File: exercise2_solution.py
# Exercise 2 Solution: Daily Motivation

from datetime import date

def daily_motivation():
    """Print daily motivation message"""
    print("=" * 50)
    print("DAILY MOTIVATION")
    print("=" * 50)
    
    # Motivational quote
    print("\n💪 Today's Quote:")
    print('"The expert in anything was once a beginner."')
    
    # Today's date
    today = date.today()
    print(f"\n📅 Date: {today.strftime('%B %d, %Y')}")
    
    # Encouraging message
    print("\n🚀 Remember:")
    print("Every line of code you write is progress!")
    print("You're building skills that will last a lifetime!")
    print("Keep going - you've got this!")
    print("=" * 50)

# Call the function
daily_motivation()
