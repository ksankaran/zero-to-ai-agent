# type_checking.py
# From: Zero to AI Agent, Chapter 2, Section 2.5
# Discovering the types of different values

# Check basic types
print("=== Basic Type Checking ===")
print(f"Type of 42: {type(42)}")                    # <class 'int'>
print(f"Type of 3.14: {type(3.14)}")               # <class 'float'>
print(f"Type of 'hello': {type('hello')}")         # <class 'str'>
print(f"Type of True: {type(True)}")               # <class 'bool'>

# Variables hold values, type() checks the value
age = 25
name = "Alice"
height = 5.7
is_student = False

print("\n=== Variable Type Checking ===")
print(f"age ({age}) is type: {type(age)}")
print(f"name ({name}) is type: {type(name)}")
print(f"height ({height}) is type: {type(height)}")
print(f"is_student ({is_student}) is type: {type(is_student)}")

# Types can change!
print("\n=== Dynamic Typing ===")
x = 42
print(f"x = {x}, type: {type(x)}")

x = "forty-two"
print(f"x = {x}, type: {type(x)}")

x = 42.0
print(f"x = {x}, type: {type(x)}")

# Using isinstance() to check types
print("\n=== Using isinstance() ===")
value = 10
print(f"Is {value} an int? {isinstance(value, int)}")
print(f"Is {value} a float? {isinstance(value, float)}")
print(f"Is {value} a string? {isinstance(value, str)}")
print(f"Is {value} a number? {isinstance(value, (int, float))}")  # Check multiple types
