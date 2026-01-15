# From: Zero to AI Agent, Chapter 5, Section 5.3
# File: none_return.py

def no_return():
    x = 5 + 3  # Does something but doesn't return

result = no_return()
print(f"Result: {result}")  # Result: None
print(f"Type: {type(result)}")  # Type: <class 'NoneType'>

# You can explicitly return None too
def maybe_divide(a, b):
    if b == 0:
        return None  # Can't divide by zero
    return a / b

result1 = maybe_divide(10, 2)
result2 = maybe_divide(10, 0)

print(f"10 / 2 = {result1}")  # 10 / 2 = 5.0
print(f"10 / 0 = {result2}")  # 10 / 0 = None