# From: Zero to AI Agent, Chapter 5, Section 5.2
# File: parameter_argument_connection.py

def calculate_rectangle_area(width, height):
    """Calculate the area of a rectangle"""
    area = width * height
    print(f"Rectangle: {width} × {height} = {area} square units")
    
# When we call this function:
calculate_rectangle_area(10, 5)

# Here's what Python does behind the scenes:
# 1. width = 10  (first argument → first parameter)
# 2. height = 5  (second argument → second parameter)
# 3. Runs the function body with these values
# 4. Prints: "Rectangle: 10 × 5 = 50 square units"
