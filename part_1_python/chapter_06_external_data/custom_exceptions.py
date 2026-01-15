# From: Zero to AI Agent, Chapter 6, Section 6.4
# File: 04_custom_exceptions.py


def validate_age(age):
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError(f"Age {age} seems unrealistic")
    return True

def get_user_age():
    while True:
        try:
            age_str = input("Enter age: ")
            age = int(age_str)
            validate_age(age)
            return age
        except ValueError as e:
            if "invalid literal" in str(e):
                print("Please enter a number")
            else:
                print(f"Invalid age: {e}")
        except TypeError as e:
            print(f"Type error: {e}")
