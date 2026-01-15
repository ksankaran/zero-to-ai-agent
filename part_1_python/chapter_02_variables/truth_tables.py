# truth_tables.py
# From: Zero to AI Agent, Chapter 2, Section 2.4
# Visualizing how logical operators work

print("=== AND Truth Table ===")
print("A     | B     | A and B")
print("------|-------|--------")
print(f"True  | True  | {True and True}")
print(f"True  | False | {True and False}")
print(f"False | True  | {False and True}")
print(f"False | False | {False and False}")

print("\n=== OR Truth Table ===")
print("A     | B     | A or B")
print("------|-------|-------")
print(f"True  | True  | {True or True}")
print(f"True  | False | {True or False}")
print(f"False | True  | {False or True}")
print(f"False | False | {False or False}")

print("\n=== NOT Truth Table ===")
print("A     | not A")
print("------|------")
print(f"True  | {not True}")
print(f"False | {not False}")
