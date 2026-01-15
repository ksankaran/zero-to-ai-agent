# From: Zero to AI Agent, Chapter 5, Section 5.2
# File: multiple_parameters.py

def introduce_person(name, age, city):
    """Introduce someone with multiple pieces of information"""
    print(f"Meet {name}!")
    print(f"They are {age} years old.")
    print(f"They live in {city}.")
    print("-" * 30)

# Call with three arguments
introduce_person("Sarah", 28, "New York")
introduce_person("James", 35, "London")
introduce_person("Yuki", 42, "Tokyo")
