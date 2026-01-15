# From: Zero to AI Agent, Chapter 5, Section 5.1
# File: welcome_program.py
# Topic: Functions can do multiple things

def run_welcome_program():
    """This function runs a complete welcome program"""
    print("=" * 40)
    print("Welcome to the Python Learning System!")
    print("=" * 40)
    
    # Functions can use variables
    user_name = input("What's your name? ")
    
    # Functions can use if statements
    if user_name.lower() == "python":
        print("Hey, that's the name of this programming language!")
    else:
        print(f"Nice to meet you, {user_name}!")
    
    # Functions can use loops
    print("\nHere are 3 reasons to love functions:")
    reasons = [
        "They make code reusable",
        "They make code organized", 
        "They make debugging easier"
    ]
    for i, reason in enumerate(reasons, 1):
        print(f"{i}. {reason}")
    
    print("\nProgram complete!")

# Call the function to run it
run_welcome_program()

# Want to run it again? Just call it again!
print("\n" + "="*40)
print("Running the program a second time:")
print("="*40 + "\n")
run_welcome_program()
