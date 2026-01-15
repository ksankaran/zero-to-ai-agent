# From: Zero to AI Agent, Chapter 6, Section 6.1
# Exercise 2 Solution: Simple Shopping List

"""
Simple Shopping List
Build a shopping list that saves items to a file.
"""

def add_item():
    """Add item to shopping list"""
    item = input("Enter item to add: ")
    with open("shopping_list.txt", "a") as file:
        file.write(item + "\n")
    print(f"✅ Added '{item}' to list")

def view_list():
    """View all items in shopping list"""
    try:
        with open("shopping_list.txt", "r") as file:
            items = file.readlines()
            if items:
                print("\n🛒 Shopping List:")
                for i, item in enumerate(items, 1):
                    print(f"  {i}. {item.strip()}")
            else:
                print("Shopping list is empty!")
    except FileNotFoundError:
        print("No shopping list yet! Add items first.")

def clear_list():
    """Clear the shopping list"""
    confirm = input("Clear entire list? (yes/no): ")
    if confirm.lower() == "yes":
        with open("shopping_list.txt", "w") as file:
            file.write("")  # Empty file
        print("✅ List cleared!")

def main():
    while True:
        print("\n=== Shopping List ===")
        print("1. Add item")
        print("2. View list")
        print("3. Clear list")
        print("4. Exit")
        
        choice = input("Choose (1-4): ")
        
        if choice == "1":
            add_item()
        elif choice == "2":
            view_list()
        elif choice == "3":
            clear_list()
        elif choice == "4":
            print("Happy shopping! 🛍️")
            break

if __name__ == "__main__":
    main()
