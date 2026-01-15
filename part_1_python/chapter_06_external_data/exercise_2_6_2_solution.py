# From: Zero to AI Agent, Chapter 6, Section 6.2
# Exercise 2 Solution: Settings Manager

"""
Settings Manager
Build a program that manages app settings in JSON.
"""

import json
import os

DEFAULT_SETTINGS = {
    "username": "User",
    "theme": "light",
    "font_size": 12
}

def load_settings():
    """Load settings from file or use defaults"""
    if os.path.exists("settings.json"):
        try:
            with open("settings.json", "r") as file:
                return json.load(file)
        except:
            return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """Save settings to JSON file"""
    with open("settings.json", "w") as file:
        json.dump(settings, file, indent=4)
    print("✅ Settings saved!")

def display_settings(settings):
    """Show current settings"""
    print("\n⚙️ Current Settings:")
    for key, value in settings.items():
        print(f"  {key}: {value}")

def change_setting(settings):
    """Change a setting"""
    print("\nAvailable settings:")
    keys = list(settings.keys())
    for i, key in enumerate(keys, 1):
        print(f"{i}. {key}")
    
    try:
        choice = int(input("Choose setting to change (number): ")) - 1
        if 0 <= choice < len(keys):
            key = keys[choice]
            
            # Get appropriate input based on setting type
            if key == "font_size":
                new_value = int(input(f"New {key} (number): "))
            else:
                new_value = input(f"New {key}: ")
            
            settings[key] = new_value
            save_settings(settings)
        else:
            print("Invalid choice!")
    except ValueError:
        print("Please enter a number!")

def main():
    settings = load_settings()
    
    while True:
        print("\n=== Settings Manager ===")
        print("1. View settings")
        print("2. Change setting")
        print("3. Reset to defaults")
        print("4. Exit")
        
        choice = input("Choose (1-4): ")
        
        if choice == "1":
            display_settings(settings)
        elif choice == "2":
            change_setting(settings)
        elif choice == "3":
            settings = DEFAULT_SETTINGS.copy()
            save_settings(settings)
            print("✅ Reset to defaults!")
        elif choice == "4":
            print("Goodbye! ⚙️")
            break

if __name__ == "__main__":
    main()
