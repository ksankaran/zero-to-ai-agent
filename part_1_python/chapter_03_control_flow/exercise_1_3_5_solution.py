# From: Zero to AI Agent, Chapter 3, Section 3.5
# Exercise 1: Number Guessing Game
# A number guessing game with hints and attempt tracking

import random

print("=" * 40)
print("NUMBER GUESSING GAME")
print("=" * 40)
print("I'm thinking of a number between 1 and 100!")
print("Can you guess it?")
print("")

# Generate random number
secret_number = random.randint(1, 100)
attempts = 0
max_attempts = 10
found = False

while attempts < max_attempts:
    guess = int(input(f"Attempt {attempts + 1}/{max_attempts} - Your guess: "))
    attempts = attempts + 1

    if guess == secret_number:
        print(f"\nCongratulations! You got it in {attempts} attempts!")
        if attempts <= 3:
            print("Amazing! You're a mind reader!")
        elif attempts <= 6:
            print("Great job! Well done!")
        else:
            print("Good persistence!")
        found = True
        break
    elif guess < secret_number:
        print("Too low! Try a higher number.")
        if abs(guess - secret_number) <= 5:
            print("   (You're very close!)")
    else:
        print("Too high! Try a lower number.")
        if abs(guess - secret_number) <= 5:
            print("   (You're very close!)")

    # Warn when running out of attempts
    remaining = max_attempts - attempts
    if remaining == 1:
        print("Warning: Last chance!")
    elif remaining <= 3:
        print(f"Warning: Only {remaining} attempts left!")

# If loop ended without finding
if not found:
    print(f"\nSorry! The number was {secret_number}.")
    print("Better luck next time!")

print("=" * 40)
