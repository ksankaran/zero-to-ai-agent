# Save as: exercise_1_1_6_solution.py
"""
Exercise 1.6.1 Solution: Understanding Script Flow

This script demonstrates how Python scripts execute from top to bottom.
Each step is numbered to show the sequential flow.

Key concept: Scripts run in ORDER. You can't skip ahead or go back.
This is different from notebooks where you can run cells out of order.
"""


def main():
    """Demonstrate sequential script execution."""
    
    print("=" * 60)
    print("🔄 UNDERSTANDING SCRIPT FLOW")
    print("=" * 60)
    print("\nWatch how this script runs from top to bottom!\n")
    
    # Step 1: First thing that happens
    print("1️⃣ Scripts start at the top - this line runs first")
    
    # Step 2: Variables are created in order
    print("2️⃣ Now we create a variable...")
    message = "Hello from step 2!"
    print(f"   Created: message = '{message}'")
    
    # Step 3: We can use variables from earlier steps
    print("3️⃣ We can use variables from previous steps")
    print(f"   Using message: {message}")
    
    # Step 4: User input pauses execution
    print("\n4️⃣ Getting user input pauses the script...")
    name = input("   What's your name? ")
    print(f"   Got it! You entered: {name}")
    
    # Step 5: More processing happens in sequence
    print("\n5️⃣ Processing continues in order...")
    greeting = f"Nice to meet you, {name}!"
    print(f"   Created greeting: {greeting}")
    
    # Step 6: Another input
    print("\n6️⃣ Another input to demonstrate order...")
    try:
        number = int(input("   Pick a number between 1-10: "))
        result = number * 2
        print(f"   {number} × 2 = {result}")
    except ValueError:
        print("   That wasn't a number, but the script continues!")
        result = 0
    
    # Step 7: We can only use variables that were created BEFORE this line
    print("\n7️⃣ Using all our variables...")
    print(f"   message: {message}")
    print(f"   name: {name}")
    print(f"   greeting: {greeting}")
    print(f"   result: {result}")
    
    # Step 8: Final step
    print("\n8️⃣ Scripts end at the bottom - this is the last step!")
    
    # Summary
    print("\n" + "=" * 60)
    print("📝 KEY POINTS ABOUT SCRIPT FLOW:")
    print("=" * 60)
    print("""
    • Scripts run TOP to BOTTOM, always
    • Each line executes in sequence (1→2→3→4...)
    • Variables must be created BEFORE they're used
    • Input pauses execution until user responds
    • You can't skip ahead or go back
    • This is DIFFERENT from notebooks where you control order
    
    In a notebook, you COULD run cell 7 before cell 4,
    but in a script, that's impossible - it's sequential!
    """)
    
    print("=" * 60)
    print("🎉 Script complete! Everything ran in order.")
    print("=" * 60)


# This special line ensures main() runs when we execute the script
if __name__ == "__main__":
    main()
