# From: Zero to AI Agent, Chapter 3, Section 3.2
# age_category.py

age = int(input("Enter your age: "))

if 0 <= age < 13:
    print("Child")
elif 13 <= age < 20:
    print("Teenager")
elif 20 <= age < 60:
    print("Adult")
elif age >= 60:
    print("Senior")
else:
    print("Invalid age!")
