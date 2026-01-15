# handling_input.py
# From: Zero to AI Agent, Chapter 2, Section 2.6
# Dealing with messy user input

print("=" * 40)
print("HANDLING USER INPUT")
print("=" * 40)

# Problem 1: Extra spaces
print("\n--- Cleaning Extra Spaces ---")
username = input("Enter username: ")  # User might type "  john  "
username_clean = username.strip()
print(f"Raw input: '{username}'")
print(f"Cleaned: '{username_clean}'")

# Problem 2: Case sensitivity
print("\n--- Handling Case Sensitivity ---")
answer = input("Do you like Python? ").strip().lower()
print(f"Your answer (cleaned): '{answer}'")
is_yes = answer == "yes" or answer == "y"
print(f"Interpreted as yes: {is_yes}")

# Problem 3: Checking if input is valid
print("\n--- Validating Number Input ---")
age_text = input("Enter your age: ").strip()
is_valid_age = age_text.isdigit()
print(f"You entered: '{age_text}'")
print(f"Is this a valid age (all digits)? {is_valid_age}")

# Note: In Chapter 3, we'll learn how to use if/else
# to do different things based on whether input is valid!
print("")
print("=" * 40)
print("In Chapter 3, you'll learn to use if/else")
print("to handle valid vs invalid input differently!")
print("=" * 40)
