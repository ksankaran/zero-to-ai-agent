# From: Zero to AI Agent, Chapter 3, Section 3.5
# countdown_timer.py

import time  # This lets us pause the program

seconds = int(input("Enter countdown seconds: "))

while seconds > 0:
    print(f"{seconds}...")
    time.sleep(1)  # Wait 1 second
    seconds = seconds - 1  # or seconds -= 1

print("⏰ Time's up!")
