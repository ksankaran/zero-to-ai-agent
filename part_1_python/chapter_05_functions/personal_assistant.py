# From: Zero to AI Agent, Chapter 5, Section 5.7
# File: personal_assistant.py

# file: personal_assistant.py
"""
Personal Assistant Module
A helpful assistant that manages tasks, passwords, and more!
"""

import json
import random
import string
from datetime import datetime, timedelta
import os

class PersonalAssistant:
    """Your personal Python assistant"""
    
    def __init__(self, name="PyAssistant", data_file="assistant_data.json"):
        self.name = name
        self.data_file = data_file
        self.tasks = []
        self.reminders = []
        self.load_data()
    
    def greet(self):
        """Greet based on time of day"""
        hour = datetime.now().hour
        if hour < 12:
            return f"Good morning! I'm {self.name}"
        elif hour < 18:
            return f"Good afternoon! I'm {self.name}"
        else:
            return f"Good evening! I'm {self.name}"
    
    def add_task(self, task):
        """Add a task to the to-do list"""
        task_item = {
            "task": task,
            "created": datetime.now().isoformat(),
            "completed": False
        }
        self.tasks.append(task_item)
        self.save_data()
        return f"Added task: {task}"
    
    def save_data(self):
        """Save assistant data to file"""
        data = {
            "tasks": self.tasks,
            "reminders": self.reminders,
            "last_saved": datetime.now().isoformat()
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self):
        """Load assistant data from file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.tasks = data.get("tasks", [])
                self.reminders = data.get("reminders", [])

def generate_strong_password(length=12):
    """Generate a secure password"""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def days_until(target_date):
    """Calculate days until a date"""
    if isinstance(target_date, str):
        target_date = datetime.strptime(target_date, "%Y-%m-%d")
    delta = target_date - datetime.now()
    return delta.days

def create_backup(source_dir, backup_dir):
    """Create a backup of a directory"""
    import shutil
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"backup_{timestamp}")
    shutil.copytree(source_dir, backup_path)
    return backup_path

def encrypt_text(text, shift=3):
    """Simple Caesar cipher encryption"""
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

def file_organizer(directory):
    """Organize files by extension"""
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            extension = os.path.splitext(filename)[1][1:]  # Get extension without dot
            if extension:
                ext_dir = os.path.join(directory, extension)
                os.makedirs(ext_dir, exist_ok=True)
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(ext_dir, filename)
                os.rename(old_path, new_path)

# Command-line interface
def main():
    print("🤖 Personal Assistant Module")
    print("-" * 40)
    
    assistant = PersonalAssistant()
    print(assistant.greet())
    
    while True:
        print("\nOptions:")
        print("1. Add task")
        print("2. Generate password")
        print("3. Calculate days until")
        print("4. Quit")
        
        choice = input("\nYour choice: ")
        
        if choice == "1":
            task = input("Enter task: ")
            print(assistant.add_task(task))
        elif choice == "2":
            length = int(input("Password length (default 12): ") or 12)
            print(f"Generated password: {generate_strong_password(length)}")
        elif choice == "3":
            date_str = input("Enter date (YYYY-MM-DD): ")
            days = days_until(date_str)
            print(f"Days until {date_str}: {days}")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
