# From: Zero to AI Agent, Chapter 6, Section 6.2
# Exercise 1 Solution: Simple Contact Book

"""
Simple Contact Book
Create a contact book that saves to JSON.
"""

import json
import os

def load_contacts():
    """Load contacts from JSON file"""
    if os.path.exists("contacts.json"):
        try:
            with open("contacts.json", "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []

def save_contacts(contacts):
    """Save contacts to JSON file"""
    with open("contacts.json", "w") as file:
        json.dump(contacts, file, indent=4)

def add_contact(contacts):
    """Add a new contact"""
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    
    contact = {
        "name": name,
        "phone": phone,
        "email": email
    }
    
    contacts.append(contact)
    save_contacts(contacts)
    print(f"✅ Added {name} to contacts!")

def view_contacts(contacts):
    """View all contacts"""
    if not contacts:
        print("No contacts yet!")
        return
    
    print("\n📱 Contact Book:")
    for i, contact in enumerate(contacts, 1):
        print(f"\n{i}. {contact['name']}")
        print(f"   Phone: {contact['phone']}")
        print(f"   Email: {contact['email']}")

def find_contact(contacts):
    """Find a contact by name"""
    search = input("Enter name to search: ").lower()
    found = False
    
    for contact in contacts:
        if search in contact['name'].lower():
            print(f"\nFound: {contact['name']}")
            print(f"Phone: {contact['phone']}")
            print(f"Email: {contact['email']}")
            found = True
    
    if not found:
        print("Contact not found!")

def main():
    contacts = load_contacts()
    
    while True:
        print("\n=== Contact Book ===")
        print("1. Add contact")
        print("2. View all")
        print("3. Find contact")
        print("4. Exit")
        
        choice = input("Choose (1-4): ")
        
        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            find_contact(contacts)
        elif choice == "4":
            print("Goodbye! 📱")
            break

if __name__ == "__main__":
    main()
