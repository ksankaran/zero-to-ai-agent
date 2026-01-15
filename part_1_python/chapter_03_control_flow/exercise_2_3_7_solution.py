# From: Zero to AI Agent, Chapter 3, Section 3.7
# Exercise 2: Star Pattern Printer
# Print various star patterns using nested loops

print("=" * 40)
print("STAR PATTERN PRINTER")
print("=" * 40)

while True:
    print("")
    print("Choose a pattern:")
    print("1) Right triangle")
    print("2) Inverted triangle")
    print("3) Diamond")
    print("4) Quit")

    choice = input("\nYour choice (1-4): ").strip()

    if choice == "4":
        print("Thanks for using Star Pattern Printer!")
        break

    if choice not in ["1", "2", "3"]:
        print("Invalid choice! Please select 1-4.")
        continue

    size = int(input("Enter pattern size (3-10): "))
    if size < 3 or size > 10:
        print("Please enter a size between 3 and 10!")
        continue

    print("")  # Blank line before pattern

    if choice == "1":
        # Right triangle
        print("Right Triangle:")
        for i in range(1, size + 1):
            for j in range(i):
                print("*", end=" ")
            print()

    elif choice == "2":
        # Inverted triangle
        print("Inverted Triangle:")
        for i in range(size, 0, -1):
            for j in range(i):
                print("*", end=" ")
            print()

    elif choice == "3":
        # Diamond
        print("Diamond:")
        # Upper half
        for i in range(1, size + 1):
            # Print spaces
            for j in range(size - i):
                print(" ", end="")
            # Print stars
            for j in range(i):
                print("* ", end="")
            print()

        # Lower half
        for i in range(size - 1, 0, -1):
            # Print spaces
            for j in range(size - i):
                print(" ", end="")
            # Print stars
            for j in range(i):
                print("* ", end="")
            print()

print("=" * 40)
