# From: Zero to AI Agent, Chapter 3, Section 3.6
# Exercise 2: Menu System with Pass
# Demonstrates break, continue, and pass keywords

print("=" * 40)
print("CALCULATOR MENU SYSTEM")
print("=" * 40)

while True:
    print("")
    print("Main Menu:")
    print("1) Calculate (add two numbers)")
    print("2) Convert (coming soon)")
    print("3) Analyze (coming soon)")
    print("4) Quit")

    choice = input("\nSelect option (1-4): ").strip()

    if choice == "1":
        # Implemented feature
        print("")
        print("ADDITION CALCULATOR")
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = num1 + num2
        print(f"Result: {num1} + {num2} = {result}")

    elif choice == "2":
        # Placeholder with pass
        print("")
        print("CONVERT FEATURE")
        pass  # TODO: Implement conversion logic
        print("This feature is coming soon!")
        print("Check back in the next update.")

    elif choice == "3":
        # Another placeholder with pass
        print("")
        print("ANALYZE FEATURE")
        pass  # TODO: Implement analysis logic
        print("This feature is under development!")
        print("It will analyze your data when ready.")

    elif choice == "4":
        print("")
        print("Thank you for using Calculator!")
        print("Goodbye!")
        break  # Exit the menu loop

    else:
        print("")
        print("Invalid choice! Please select 1-4.")
        continue  # Skip to next iteration

    # Ask if user wants to continue
    if choice in ["1", "2", "3"]:
        another = input("\nReturn to menu? (yes/no): ").lower()
        if another != "yes":
            print("Goodbye!")
            break

print("=" * 40)
