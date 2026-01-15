# From: Zero to AI Agent, Chapter 3, Section 3.6
# password_checker.py

print("🔐 Secure Password System")
print("You have 3 attempts.\n")

correct_password = "AI2024"
max_attempts = 3

for attempt in range(1, max_attempts + 1):
    password = input(f"Attempt {attempt}: Enter password: ")
    
    if password == correct_password:
        print("✅ Access granted! Welcome to the AI system.")
        break  # Exit the loop early - we're done!
    else:
        remaining = max_attempts - attempt
        if remaining > 0:
            print(f"❌ Wrong password. {remaining} attempts remaining.\n")
else:
    # This else belongs to the for loop, not the if!
    # It runs if the loop completes without breaking
    print("\n🚫 Access denied. Too many failed attempts.")
