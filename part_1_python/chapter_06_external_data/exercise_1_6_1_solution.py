# From: Zero to AI Agent, Chapter 6, Section 6.1
# Exercise 1 Solution: Daily Note Taker

"""
Daily Note Taker
Create a simple program that lets you write a daily note to a file.
"""

from datetime import datetime

def add_note():
    """Add a note with timestamp to the file"""
    # Get note from user
    note = input("Enter your note: ")
    
    # Get current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Format the note with timestamp
    formatted_note = f"[{timestamp}] {note}\n"
    
    # Append to file (creates file if it doesn't exist)
    with open("daily_notes.txt", "a") as file:
        file.write(formatted_note)
    
    print("✅ Note saved!")

def view_notes():
    """Display all notes"""
    try:
        with open("daily_notes.txt", "r") as file:
            notes = file.read()
            if notes:
                print("\n📝 Your Notes:")
                print("-" * 40)
                print(notes)
            else:
                print("No notes yet!")
    except FileNotFoundError:
        print("No notes file found. Add a note first!")

def main():
    """Main program"""
    while True:
        print("\n=== Daily Note Taker ===")
        print("1. Add a note")
        print("2. View all notes")
        print("3. Exit")
        
        choice = input("\nChoose (1-3): ")
        
        if choice == "1":
            add_note()
        elif choice == "2":
            view_notes()
        elif choice == "3":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
