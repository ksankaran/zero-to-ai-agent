# From: Zero to AI Agent, Chapter 5, Section 5.4
# File: global_keyword_demo.py

counter = 0  # Global variable

def increment_wrong():
    counter = counter + 1  # ERROR! Can't modify global without 'global' keyword
    
def increment_right():
    global counter  # Tell Python we want to modify the global variable
    counter = counter + 1  # Now it works!

# increment_wrong()  # This would cause an UnboundLocalError

print(f"Counter before: {counter}")  # Counter before: 0
increment_right()
print(f"Counter after: {counter}")   # Counter after: 1
increment_right()
print(f"Counter after: {counter}")   # Counter after: 2