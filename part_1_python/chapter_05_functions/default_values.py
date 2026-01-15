# From: Zero to AI Agent, Chapter 5, Section 5.2
# File: default_values.py

def make_coffee(size="medium", sugar=1, milk=False):
    """Make coffee with default preferences"""
    print(f"Making a {size} coffee...")
    print(f"Adding {sugar} spoon(s) of sugar...")
    
    if milk:
        print("Adding milk...")
    else:
        print("No milk (black coffee)...")
    
    print("☕ Your coffee is ready!")
    print("-" * 30)

# Use all defaults
make_coffee()

# Override just the size
make_coffee("large")

# Override size and sugar
make_coffee("small", 2)

# Override everything
make_coffee("large", 0, True)

# Skip parameters using keyword arguments (next section!)
make_coffee(milk=True)  # Uses default size and sugar
