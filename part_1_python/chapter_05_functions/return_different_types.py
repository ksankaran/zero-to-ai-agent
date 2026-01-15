# From: Zero to AI Agent, Chapter 5, Section 5.3
# File: return_different_types.py

# Return a number
def calculate_area(length, width):
    return length * width

# Return a string
def create_email(name, domain):
    return f"{name.lower()}@{domain}"

# Return a list
def get_factors(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

# Return a dictionary
def get_student_info(name, age, grade):
    return {
        "name": name,
        "age": age,
        "grade": grade,
        "is_adult": age >= 18
    }

# Return a boolean
def is_even(number):
    return number % 2 == 0

# Try them all!
area = calculate_area(5, 3)
print(f"Area: {area}")

email = create_email("Alice", "example.com")
print(f"Email: {email}")

factors = get_factors(12)
print(f"Factors of 12: {factors}")

student = get_student_info("Bob", 17, "A")
print(f"Student info: {student}")

if is_even(42):
    print("42 is even!")