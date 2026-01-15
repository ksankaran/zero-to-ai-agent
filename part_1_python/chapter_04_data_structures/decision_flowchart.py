# From: Zero to AI Agent, Chapter 4, Section 4.6
# decision_flowchart.py - Step-by-step decision process for choosing data structures
# Demonstrates the decision process without functions

print("=" * 40)
print("DATA STRUCTURE DECISION FLOWCHART")
print("=" * 40)

# The decision process:
# 1. Do you need key-value pairs? -> DICTIONARY
# 2. Do you need uniqueness? -> SET
# 3. Will the data change? -> LIST (if yes) or TUPLE (if no)

# Scenario 1: User profiles with lookup by ID
print("\nScenario 1: User profiles with lookup by ID")
print("  Question: Do you need key-value pairs? YES")
print("  Answer: Use DICTIONARY")
example_1 = {"user_123": {"name": "Alice", "age": 25}}
print(f"  Example: {example_1}")

# Scenario 2: Unique visitor tracking
print("\nScenario 2: Unique visitor tracking")
print("  Question: Do you need key-value pairs? NO")
print("  Question: Do you need uniqueness? YES")
print("  Answer: Use SET")
example_2 = {"visitor_1", "visitor_2", "visitor_3"}
print(f"  Example: {example_2}")

# Scenario 3: Shopping cart that changes
print("\nScenario 3: Shopping cart that changes")
print("  Question: Do you need key-value pairs? NO")
print("  Question: Do you need uniqueness? NO")
print("  Question: Will the data change? YES")
print("  Answer: Use LIST")
example_3 = ["apple", "banana", "milk"]
print(f"  Example: {example_3}")

# Scenario 4: GPS coordinates that never change
print("\nScenario 4: GPS coordinates that never change")
print("  Question: Do you need key-value pairs? NO")
print("  Question: Do you need uniqueness? NO")
print("  Question: Will the data change? NO")
print("  Answer: Use TUPLE")
example_4 = (37.7749, -122.4194)
print(f"  Example: {example_4}")

# Interactive decision helper
print("\n" + "=" * 40)
print("INTERACTIVE DECISION HELPER")
print("=" * 40)

needs_key_value = input("Do you need key-value pairs? (yes/no): ").lower().strip() == "yes"

if needs_key_value:
    print("\nRecommendation: Use DICTIONARY")
    print("Example: my_dict = {'key': 'value'}")
else:
    needs_unique = input("Do you need uniqueness (no duplicates)? (yes/no): ").lower().strip() == "yes"

    if needs_unique:
        print("\nRecommendation: Use SET")
        print("Example: my_set = {1, 2, 3}")
    else:
        will_change = input("Will the data change after creation? (yes/no): ").lower().strip() == "yes"

        if will_change:
            print("\nRecommendation: Use LIST")
            print("Example: my_list = [1, 2, 3]")
        else:
            print("\nRecommendation: Use TUPLE")
            print("Example: my_tuple = (1, 2, 3)")

print("=" * 40)
