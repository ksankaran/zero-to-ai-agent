# From: Zero to AI Agent, Chapter 5, Section 5.4
# File: legb_rule_demo.py

# Global scope
x = "global"

def outer():
    # Enclosing scope
    x = "enclosing"
    
    def inner():
        # Local scope
        x = "local"
        print(f"Inner function sees: {x}")  # Prints: local
    
    inner()
    print(f"Outer function sees: {x}")  # Prints: enclosing

outer()
print(f"Global scope sees: {x}")  # Prints: global