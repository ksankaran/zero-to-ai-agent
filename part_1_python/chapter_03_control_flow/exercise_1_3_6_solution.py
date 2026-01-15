# From: Zero to AI Agent, Chapter 3, Section 3.6
# Exercise 1: Search and Stop
# Guess the secret word with break and continue

print("=" * 40)
print("SEARCH AND STOP - WORD GUESSING GAME")
print("=" * 40)

secret_word = "python"
max_attempts = 5
attempts_used = 0
found = False

print("I'm thinking of a programming-related word.")
print(f"You have {max_attempts} attempts to guess it!")
print("")

for attempt in range(1, max_attempts + 1):
    guess = input(f"Attempt {attempt}: ").strip().lower()

    # Skip empty guesses using continue
    if guess == "":
        print("  Empty guess - skipping (doesn't count as attempt)")
        continue

    attempts_used = attempts_used + 1

    # Check the guess
    if guess == secret_word:
        print(f"\nCorrect! You got it in {attempts_used} attempts!")
        print(f"The word was '{secret_word}'")
        found = True
        break  # Exit early - found the word!
    else:
        # Give hints based on length
        if len(guess) < len(secret_word):
            print(f"  Wrong! Hint: The word is longer than '{guess}'")
        elif len(guess) > len(secret_word):
            print(f"  Wrong! Hint: The word is shorter than '{guess}'")
        else:
            print(f"  Wrong! Hint: Right length, wrong word")

# If loop completed without finding
if not found:
    print(f"\nSorry! You've used all {max_attempts} attempts.")
    print(f"The secret word was: '{secret_word}'")
    print("Better luck next time!")

print("=" * 40)
