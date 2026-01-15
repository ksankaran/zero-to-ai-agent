# truthy_falsy.py
# From: Zero to AI Agent, Chapter 2, Section 2.4
# Understanding what Python considers True or False

print("=== Values That Act Like False (Falsy) ===")
# These all act like False in boolean contexts:
print(f"bool(False): {bool(False)}")      # False itself
print(f"bool(0): {bool(0)}")              # Zero
print(f"bool(0.0): {bool(0.0)}")          # Zero float
print(f"bool(''): {bool('')}")            # Empty string
print(f"bool([]): {bool([])}")            # Empty list
print(f"bool(None): {bool(None)}")        # None

print("\n=== Values That Act Like True (Truthy) ===")
# These all act like True:
print(f"bool(True): {bool(True)}")        # True itself
print(f"bool(1): {bool(1)}")              # Non-zero number
print(f"bool(-5): {bool(-5)}")            # Negative numbers too
print(f"bool('hello'): {bool('hello')}")  # Non-empty string
print(f"bool(' '): {bool(' ')}")          # Even just a space!
print(f"bool([0]): {bool([0])}")          # Non-empty list

# Practical application
user_input = ""  # Empty string is falsy
has_input = bool(user_input)
print(f"\nUser input: '{user_input}'")
print(f"Has input? {has_input}")

user_input = "Alice"  # Non-empty string is truthy
has_input = bool(user_input)
print(f"\nUser input: '{user_input}'")
print(f"Has input? {has_input}")
