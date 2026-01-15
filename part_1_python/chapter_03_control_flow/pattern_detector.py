# From: Zero to AI Agent, Chapter 3, Section 3.7
# pattern_detector.py

print("🔍 Pattern Detection System")
print("We'll check a 3x3 grid for patterns\n")

# Get a 3x3 grid of values from the user
print("Enter 1 for filled, 0 for empty:")
row1_col1 = int(input("Row 1, Column 1: "))
row1_col2 = int(input("Row 1, Column 2: "))
row1_col3 = int(input("Row 1, Column 3: "))

row2_col1 = int(input("Row 2, Column 1: "))
row2_col2 = int(input("Row 2, Column 2: "))
row2_col3 = int(input("Row 2, Column 3: "))

row3_col1 = int(input("Row 3, Column 1: "))
row3_col2 = int(input("Row 3, Column 2: "))
row3_col3 = int(input("Row 3, Column 3: "))

print("\nYour grid:")
print(f"{row1_col1} {row1_col2} {row1_col3}")
print(f"{row2_col1} {row2_col2} {row2_col3}")
print(f"{row3_col1} {row3_col2} {row3_col3}")

print("\n📊 Analyzing patterns...")

# Check for horizontal line in each row
horizontal_lines = 0
if row1_col1 == 1 and row1_col2 == 1 and row1_col3 == 1:
    horizontal_lines += 1
    print("→ Horizontal line in row 1")
if row2_col1 == 1 and row2_col2 == 1 and row2_col3 == 1:
    horizontal_lines += 1
    print("→ Horizontal line in row 2")
if row3_col1 == 1 and row3_col2 == 1 and row3_col3 == 1:
    horizontal_lines += 1
    print("→ Horizontal line in row 3")

# Check for vertical lines
vertical_lines = 0
if row1_col1 == 1 and row2_col1 == 1 and row3_col1 == 1:
    vertical_lines += 1
    print("↓ Vertical line in column 1")
if row1_col2 == 1 and row2_col2 == 1 and row3_col2 == 1:
    vertical_lines += 1
    print("↓ Vertical line in column 2")
if row1_col3 == 1 and row2_col3 == 1 and row3_col3 == 1:
    vertical_lines += 1
    print("↓ Vertical line in column 3")

# Check for diagonal
if row1_col1 == 1 and row2_col2 == 1 and row3_col3 == 1:
    print("↘ Diagonal line (top-left to bottom-right)")
if row1_col3 == 1 and row2_col2 == 1 and row3_col1 == 1:
    print("↙ Diagonal line (top-right to bottom-left)")

# Check for center pattern
if row2_col2 == 1:
    neighbors = 0
    if row1_col2 == 1: neighbors += 1
    if row2_col1 == 1: neighbors += 1
    if row2_col3 == 1: neighbors += 1
    if row3_col2 == 1: neighbors += 1
    
    if neighbors == 4:
        print("✚ Plus/Cross pattern detected!")

print(f"\n📈 Summary:")
print(f"Horizontal lines: {horizontal_lines}")
print(f"Vertical lines: {vertical_lines}")

# Pattern classification
total_filled = (row1_col1 + row1_col2 + row1_col3 + 
                row2_col1 + row2_col2 + row2_col3 + 
                row3_col1 + row3_col2 + row3_col3)

if total_filled == 0:
    print("Classification: Empty grid")
elif total_filled == 9:
    print("Classification: Full grid")
elif horizontal_lines > 0 or vertical_lines > 0:
    print("Classification: Line pattern")
else:
    print("Classification: Random pattern")
