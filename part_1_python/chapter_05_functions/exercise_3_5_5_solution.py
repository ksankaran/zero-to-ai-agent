# From: Zero to AI Agent, Chapter 5, Section 5.5
# File: exercise_3_5_5_solution.py

text_lines = [
    "  First Line  ",
    "",
    "SECOND LINE",
    "   ",
    "Third Line"
]

# Step 1: Remove whitespace
trimmed = list(map(lambda line: line.strip(), text_lines))
print(f"Trimmed: {trimmed}")

# Step 2: Filter out empty lines
non_empty = list(filter(lambda line: line != "", trimmed))
print(f"Non-empty: {non_empty}")

# Step 3: Convert to lowercase
lowercase = list(map(lambda line: line.lower(), non_empty))
print(f"Lowercase: {lowercase}")

# Step 4: Add line numbers
numbered = list(map(lambda item: f"{item[0]+1}. {item[1]}", 
                   enumerate(lowercase)))
print(f"Numbered: {numbered}")

# All in one pipeline!
processed = list(map(
    lambda item: f"{item[0]+1}. {item[1]}", 
    enumerate(
        map(lambda line: line.lower(),
            filter(lambda line: line != "",
                   map(lambda line: line.strip(), text_lines)))
    )
))

print(f"\nFinal processed lines:")
for line in processed:
    print(f"  {line}")
