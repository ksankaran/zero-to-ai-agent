# From: Zero to AI Agent, Chapter 5, Section 5.1
# File: exercise3_solution.py
# Exercise 3 Solution: Code Stats Reporter

def report_progress():
    """Report learning progress"""
    # Create list of completed chapters
    completed_chapters = [1, 2, 3, 4]
    
    # Calculate progress
    total_completed = len(completed_chapters)
    
    # Print header
    print("📚 PYTHON LEARNING PROGRESS REPORT 📚")
    print("=" * 40)
    
    # Print summary
    print(f"\nChapters Completed: {total_completed}")
    print(f"Current Chapter: 5")
    
    # List completed chapters with loop
    print("\n✅ Completed Chapters:")
    for chapter in completed_chapters:
        if chapter == 1:
            topic = "Development Environment"
        elif chapter == 2:
            topic = "Variables and Data Types"
        elif chapter == 3:
            topic = "Control Flow and Logic"
        elif chapter == 4:
            topic = "Data Structures"
        print(f"   Chapter {chapter}: {topic}")
    
    # Encouraging message
    print("\n🎯 Achievement Unlocked!")
    print("You've mastered the Python foundations!")
    print("Now you're learning to organize code with functions!")
    print("=" * 40)

# Call the function
report_progress()

# We can call it again anytime we want!
print("\n")
report_progress()
