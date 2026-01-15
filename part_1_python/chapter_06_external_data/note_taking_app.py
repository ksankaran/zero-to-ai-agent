# From: Zero to AI Agent, Chapter 6, Section 6.1
# File: note_taking_app.py

import datetime
import os

def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("📝 PYTHON NOTE-TAKING APP 📝")
    print("="*50)
    print("1. Add a new note")
    print("2. View all notes")
    print("3. Search notes")
    print("4. Clear all notes")
    print("5. Exit")
    print("-"*50)

def add_note():
    """Add a new note with timestamp"""
    note = input("\nWhat's your note? ")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("my_notes.txt", "a") as file:
        file.write(f"[{timestamp}] {note}\n")
    
    print("✅ Note saved successfully!")

def view_notes():
    """Display all notes"""
    # Check if file exists first!
    if not os.path.exists("my_notes.txt"):
        print("\n📭 No notes yet! Add your first note.")
        return
    
    with open("my_notes.txt", "r") as file:
        notes = file.read()
        if notes:
            print("\n📚 Your Notes:")
            print("-"*50)
            print(notes)
        else:
            print("\n📭 No notes yet! Add your first note.")

def search_notes():
    """Search for notes containing a keyword"""
    if not os.path.exists("my_notes.txt"):
        print("\n📭 No notes to search!")
        return
    
    keyword = input("\nSearch for: ").lower()
    found_notes = []
    
    with open("my_notes.txt", "r") as file:
        for line in file:
            if keyword in line.lower():
                found_notes.append(line.strip())
    
    if found_notes:
        print(f"\n🔍 Found {len(found_notes)} note(s) containing '{keyword}':")
        print("-"*50)
        for note in found_notes:
            print(note)
    else:
        print(f"\n❌ No notes found containing '{keyword}'")

def clear_notes():
    """Clear all notes (with confirmation)"""
    if not os.path.exists("my_notes.txt"):
        print("\n📭 No notes to clear!")
        return
    
    confirm = input("\n⚠️  Delete all notes? (yes/no): ").lower()
    if confirm == 'yes':
        with open("my_notes.txt", "w") as file:
            pass  # Opening in 'w' mode clears the file
        print("🗑️  All notes cleared!")
    else:
        print("❌ Cancelled - notes are safe!")

def main():
    """Main application loop"""
    print("Welcome to your personal note-taking app!")
    print("This is exactly how AI systems store conversation history!")
    
    while True:
        display_menu()
        choice = input("\nYour choice (1-5): ")
        
        if choice == '1':
            add_note()
        elif choice == '2':
            view_notes()
        elif choice == '3':
            search_notes()
        elif choice == '4':
            clear_notes()
        elif choice == '5':
            print("\n👋 Thanks for using the note app! Your notes are saved.")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
