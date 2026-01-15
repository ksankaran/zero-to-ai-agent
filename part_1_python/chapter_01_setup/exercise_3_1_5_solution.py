# Save as: exercise_3_1_5_solution.py
"""
Exercise 3 1.5 Solution: Days Until Python Master

This program tracks your Python learning journey and estimates
when you'll reach proficiency (100 days of practice).
"""

import datetime


def main():
    """Main function for the learning tracker."""
    
    print("=" * 60)
    print("🐍 PYTHON LEARNING TRACKER")
    print("=" * 60)
    print("\nTrack your journey to Python proficiency!")
    
    # Get start date
    print("\nWhen did you start learning Python?")
    print("  1. Today")
    print("  2. Enter a specific date")
    
    choice = input("\nYour choice (1/2): ").strip()
    
    if choice == "1":
        start_date = datetime.date.today()
    elif choice == "2":
        while True:
            try:
                date_str = input("Enter start date (YYYY-MM-DD): ").strip()
                start_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                
                # Validate date is not in the future
                if start_date > datetime.date.today():
                    print("❌ Start date can't be in the future!")
                    continue
                break
            except ValueError:
                print("❌ Please use format YYYY-MM-DD (e.g., 2024-01-15)")
    else:
        print("Invalid choice, using today's date.")
        start_date = datetime.date.today()
    
    # Calculate days of learning
    today = datetime.date.today()
    days_learning = (today - start_date).days
    
    # Proficiency target: 100 days
    PROFICIENCY_DAYS = 100
    days_remaining = max(0, PROFICIENCY_DAYS - days_learning)
    target_date = start_date + datetime.timedelta(days=PROFICIENCY_DAYS)
    
    # Calculate progress percentage
    progress = min(100, (days_learning / PROFICIENCY_DAYS) * 100)
    
    # Display results
    print("\n" + "=" * 60)
    print("📊 YOUR LEARNING PROGRESS")
    print("=" * 60)
    
    print(f"\n📅 Start Date: {start_date.strftime('%B %d, %Y')}")
    print(f"📅 Today: {today.strftime('%B %d, %Y')}")
    print(f"🎯 Target Date: {target_date.strftime('%B %d, %Y')}")
    
    print(f"\n⏱️ Days of Learning: {days_learning}")
    print(f"⏳ Days Remaining: {days_remaining}")
    
    # Progress bar
    bar_length = 30
    filled = int(bar_length * progress / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"\n📈 Progress: [{bar}] {progress:.1f}%")
    
    # Milestone messages
    print("\n" + "-" * 60)
    if progress >= 100:
        print("🎉 CONGRATULATIONS! You've reached 100 days!")
        print("   You should be feeling confident with Python basics!")
        print("   Time to tackle more advanced topics!")
    elif progress >= 75:
        print("🌟 Amazing progress! You're in the home stretch!")
        print(f"   Only {days_remaining} days to go!")
    elif progress >= 50:
        print("💪 Halfway there! Keep up the momentum!")
        print("   Consistency is key to mastery.")
    elif progress >= 25:
        print("🚀 Great start! You're building solid foundations!")
        print("   The concepts will start clicking soon.")
    elif progress > 0:
        print("🌱 You've begun your journey!")
        print("   Every expert was once a beginner.")
    else:
        print("🎬 Welcome to Day 1!")
        print("   The best time to start was yesterday.")
        print("   The second best time is NOW!")
    
    # Weekly breakdown
    weeks_total = PROFICIENCY_DAYS // 7
    weeks_done = days_learning // 7
    weeks_left = max(0, weeks_total - weeks_done)
    
    print("\n" + "-" * 60)
    print("📆 WEEKLY BREAKDOWN")
    print("-" * 60)
    print(f"   Weeks completed: {weeks_done} / {weeks_total}")
    print(f"   Weeks remaining: {weeks_left}")
    
    # Motivational tip
    tips = [
        "💡 Tip: Code every day, even if just for 15 minutes!",
        "💡 Tip: Build small projects to reinforce learning!",
        "💡 Tip: Don't just read - type out every example!",
        "💡 Tip: Explain concepts to others (or a rubber duck)!",
        "💡 Tip: Embrace errors - they're learning opportunities!",
        "💡 Tip: Join Python communities for support!",
        "💡 Tip: Review old code to see how far you've come!",
    ]
    
    # Pick a tip based on days (so it varies)
    tip_index = days_learning % len(tips)
    print(f"\n{tips[tip_index]}")
    
    # Suggested daily goal
    if days_remaining > 0:
        print("\n" + "=" * 60)
        print("🎯 TODAY'S SUGGESTION")
        print("=" * 60)
        
        if days_learning < 7:
            print("   Focus: Python basics (variables, print, input)")
        elif days_learning < 14:
            print("   Focus: Control flow (if/else, loops)")
        elif days_learning < 21:
            print("   Focus: Data structures (lists, dictionaries)")
        elif days_learning < 30:
            print("   Focus: Functions and modules")
        elif days_learning < 50:
            print("   Focus: File handling and error management")
        elif days_learning < 75:
            print("   Focus: Object-oriented programming")
        else:
            print("   Focus: Build a complete project!")
    
    print("\n" + "=" * 60)
    print("Keep coding! Every line brings you closer to mastery! 🐍")
    print("=" * 60)


if __name__ == "__main__":
    main()
