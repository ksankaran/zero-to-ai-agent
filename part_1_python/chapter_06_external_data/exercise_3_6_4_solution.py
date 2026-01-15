# From: Zero to AI Agent, Chapter 6, Section 6.4
# Exercise 3 Solution: List Index Checker

"""
List Index Checker
Create a program that safely accesses list items.
"""

def safe_list_access():
    """Safely access items in a list"""
    # Create a sample list
    items = ["apple", "banana", "orange", "grape", "mango"]
    
    print("\n📋 List contents:")
    for i, item in enumerate(items):
        print(f"  Index {i}: {item}")
    
    while True:
        try:
            # Ask for index
            user_input = input("\nEnter an index to access (0-4): ")
            
            # Convert to integer
            index = int(user_input)
            
            # Access the item
            item = items[index]
            
            print(f"✅ Item at index {index}: {item}")
            break
            
        except ValueError:
            print("❌ Please enter a number!")
            print(f"Valid range is 0 to {len(items)-1}")
            
        except IndexError:
            print(f"❌ Index {index} is out of range!")
            print(f"Valid indices are 0 to {len(items)-1}")
            
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

def main():
    print("=== List Index Checker ===")
    
    while True:
        safe_list_access()
        
        again = input("\nTry again? (yes/no): ")
        if again.lower() != 'yes':
            break
    
    print("Thanks for practicing! 🎯")

if __name__ == "__main__":
    main()
