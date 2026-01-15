# From: Zero to AI Agent, Chapter 3, Section 3.2
# password_strength_checker.py

password = input("Create a password: ")
username = input("Enter your username: ")

# Check various conditions
if len(password) < 8:
    print("❌ Password too short! Use at least 8 characters.")
elif password == username:
    print("❌ Password can't be the same as username!")
elif password.lower() == "password":
    print("❌ Really? 'password' as your password? Try again!")
else:
    print("✅ Password accepted!")
