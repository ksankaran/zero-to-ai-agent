# From: Zero to AI Agent, Chapter 5, Section 5.4
# File: local_scope_demo.py

def make_coffee():
    # These variables only exist inside make_coffee()
    coffee_type = "Espresso"
    temperature = "Hot"
    size = "Medium"
    
    print(f"Making a {temperature} {size} {coffee_type}")

make_coffee()

# Try to access them outside - won't work!
# print(coffee_type)  # NameError: name 'coffee_type' is not defined