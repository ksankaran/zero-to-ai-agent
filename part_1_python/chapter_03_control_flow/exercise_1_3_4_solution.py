# From: Zero to AI Agent, Chapter 3, Section 3.4
# Exercise 1: Countdown Timer
# Create a countdown timer using a for loop

print("=" * 40)
print("COUNTDOWN TIMER")
print("=" * 40)

# Get starting number
start = int(input("Enter starting number for countdown: "))

print(f"\nStarting countdown from {start}...")
print("-" * 40)

# Countdown loop using range with negative step
for seconds in range(start, 0, -1):
    if seconds == 1:
        print(f"T-minus {seconds} second")
    else:
        print(f"T-minus {seconds} seconds")

print("")
print("BLAST OFF!")
print("Mission launched successfully!")
print("=" * 40)
