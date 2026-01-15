# From: Zero to AI Agent, Chapter 5, Section 5.2
# File: different_types.py

def process_list(my_list):
    """Work with a list parameter"""
    print(f"You gave me a list with {len(my_list)} items:")
    for item in my_list:
        print(f"  • {item}")

def analyze_dictionary(person_dict):
    """Work with a dictionary parameter"""
    print("Person Information:")
    for key, value in person_dict.items():
        print(f"  {key}: {value}")

def check_number(number, threshold):
    """Work with number parameters"""
    if number > threshold:
        print(f"{number} is greater than {threshold}")
    else:
        print(f"{number} is not greater than {threshold}")

# Using our functions with different data types
shopping = ["apples", "bread", "cheese", "tea"]
process_list(shopping)

person = {"name": "Alex", "age": 30, "job": "Teacher"}
analyze_dictionary(person)

check_number(75, 50)
check_number(25, 50)
