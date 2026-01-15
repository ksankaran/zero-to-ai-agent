# From: Zero to AI Agent, Chapter 6, Section 6.2
# File: contact_manager_json.py

import json
import os

CONTACTS_FILE = "contacts.json"

def load_contacts():
    """Load contacts from JSON file"""
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    return []  # Return empty list if file doesn't exist

def save_contacts(contacts):
    """Save contacts to JSON file"""
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

def add_contact():
    """Add a new contact"""
    print("\n📝 Adding New Contact")
    print("-" * 30)
    
    contact = {
        "name": input("Name: ").strip(),
        "phone": input("Phone: ").strip(),
        "email": input("Email: ").strip(),
        "address": {
            "street": input("Street address: ").strip(),
            "city": input("City: ").strip(),
            "zip": input("ZIP code: ").strip()
        },
        "interests": input("Interests (comma-separated): ").strip().split(","),
        "favorite": False
    }
    
    # Clean up interests list
    contact["interests"] = [i.strip() for i in contact["interests"] if i.strip()]
    
    contacts = load_contacts()
    contacts.append(contact)
    save_contacts(contacts)
    
    print(f"✅ Added {contact['name']} to contacts!")
    return contact

def view_contacts():
    """Display all contacts"""
    contacts = load_contacts()
    
    if not contacts:
        print("\n📭 No contacts yet! Add your first contact.")
        return
    
    print(f"\n📇 Your Contacts ({len(contacts)} total)")
    print("=" * 50)
    
    for i, contact in enumerate(contacts, 1):
        favorite = "⭐" if contact.get("favorite", False) else ""
        print(f"\n{i}. {contact['name']} {favorite}")
        print(f"   📱 {contact['phone']}")
        print(f"   📧 {contact['email']}")
        
        address = contact.get('address', {})
        if address.get('street'):
            print(f"   🏠 {address['street']}, {address['city']} {address['zip']}")
        
        if contact.get('interests'):
            print(f"   💜 Interests: {', '.join(contact['interests'])}")

def search_contacts():
    """Search for contacts"""
    contacts = load_contacts()
    
    if not contacts:
        print("\n📭 No contacts to search!")
        return
    
    search_term = input("\n🔍 Search for: ").lower()
    found = []
    
    for contact in contacts:
        # Search in all text fields
        if (search_term in contact['name'].lower() or
            search_term in contact['phone'] or
            search_term in contact['email'].lower() or
            any(search_term in interest.lower() for interest in contact.get('interests', []))):
            found.append(contact)
    
    if found:
        print(f"\n✅ Found {len(found)} contact(s):")
        for contact in found:
            print(f"  • {contact['name']} - {contact['phone']}")
    else:
        print(f"\n❌ No contacts found matching '{search_term}'")

def toggle_favorite():
    """Mark/unmark a contact as favorite"""
    contacts = load_contacts()
    
    if not contacts:
        print("\n📭 No contacts yet!")
        return
    
    # Show contacts with numbers
    for i, contact in enumerate(contacts, 1):
        favorite = "⭐" if contact.get("favorite", False) else ""
        print(f"{i}. {contact['name']} {favorite}")
    
    try:
        choice = int(input("\nToggle favorite for which contact? ")) - 1
        if 0 <= choice < len(contacts):
            contacts[choice]["favorite"] = not contacts[choice].get("favorite", False)
            save_contacts(contacts)
            status = "favorited" if contacts[choice]["favorite"] else "unfavorited"
            print(f"✅ {contacts[choice]['name']} {status}!")
        else:
            print("❌ Invalid contact number")
    except ValueError:
        print("❌ Please enter a number")

def export_to_csv():
    """Export contacts to CSV format"""
    contacts = load_contacts()
    
    if not contacts:
        print("\n📭 No contacts to export!")
        return
    
    with open("contacts_export.csv", "w") as file:
        # Write header
        file.write("Name,Phone,Email,City,Interests\n")
        
        # Write contacts
        for contact in contacts:
            interests = ";".join(contact.get("interests", []))
            city = contact.get("address", {}).get("city", "")
            file.write(f"{contact['name']},{contact['phone']},{contact['email']},{city},{interests}\n")
    
    print(f"✅ Exported {len(contacts)} contacts to contacts_export.csv")

def main():
    """Main application loop"""
    print("🌟 Welcome to JSON Contact Manager!")
    print("This demonstrates how real apps store structured data")
    
    while True:
        print("\n" + "="*50)
        print("📇 CONTACT MANAGER")
        print("="*50)
        print("1. Add new contact")
        print("2. View all contacts")
        print("3. Search contacts")
        print("4. Toggle favorite")
        print("5. Export to CSV")
        print("6. Exit")
        
        choice = input("\nYour choice: ")
        
        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contacts()
        elif choice == "4":
            toggle_favorite()
        elif choice == "5":
            export_to_csv()
        elif choice == "6":
            contacts = load_contacts()
            print(f"\n👋 Goodbye! {len(contacts)} contacts saved in {CONTACTS_FILE}")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
