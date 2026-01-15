# From: Zero to AI Agent, Chapter 3, Section 3.3
# flexible_login_system.py

username = input("Username: ")
email = input("Email: ")
phone = input("Phone (last 4 digits): ")

# User can log in with username OR email OR phone
if username == "admin" or email == "admin@ai.com" or phone == "1234":
    print("✅ Login successful!")
    print("Welcome back to your AI Dashboard!")
else:
    print("❌ Login failed. Please check your credentials.")
