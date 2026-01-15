# Exercise 2: Personal Info Card
# Create a personal info card with nice formatting

# Solution:

# Personal information
first_name = "Alexandra"
last_name = "Johnson"
age = 28
city = "San Francisco"
occupation = "Software Engineer"
email = "alex.johnson@email.com"
phone = "555-0123"
skills = "Python, JavaScript, SQL"

# Create formatted card
print("╔" + "═" * 48 + "╗")
print("║" + " PERSONAL INFORMATION CARD ".center(48) + "║")
print("╠" + "═" * 48 + "╣")

# Format each line
print(f"║ {'Name:':<15} {first_name} {last_name:<26} ║")
print(f"║ {'Age:':<15} {age:<33} ║")
print(f"║ {'Location:':<15} {city:<33} ║")
print(f"║ {'Occupation:':<15} {occupation:<33} ║")

print("╠" + "═" * 48 + "╣")
print("║" + " CONTACT INFORMATION ".center(48) + "║")
print("╠" + "═" * 48 + "╣")

print(f"║ {'Email:':<15} {email:<33} ║")
print(f"║ {'Phone:':<15} {phone:<33} ║")

print("╠" + "═" * 48 + "╣")
print("║" + " SKILLS ".center(48) + "║")
print("╠" + "═" * 48 + "╣")

print(f"║ {skills:^48} ║")
print("╚" + "═" * 48 + "╝")

# Alternative simple version
print("\n--- Simple Version ---")
print(f"Name: {first_name} {last_name}")
print(f"Age: {age} | Location: {city}")
print(f"Job: {occupation}")
print(f"Contact: {email} | {phone}")
print(f"Skills: {skills}")
