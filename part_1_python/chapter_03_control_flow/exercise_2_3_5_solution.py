# From: Zero to AI Agent, Chapter 3, Section 3.5
# Exercise 2: Input Accumulator
# Accumulate numbers until 'done' is typed (without using lists)

print("=" * 40)
print("NUMBER ACCUMULATOR")
print("=" * 40)
print("Enter numbers one at a time.")
print("Type 'done' when finished.")
print("")

# Track running statistics (without storing all values in a list)
count = 0
total = 0
minimum = None
maximum = None

while True:
    user_input = input("Enter a number (or 'done'): ").strip()

    if user_input.lower() == 'done':
        break

    # Convert to number
    number = float(user_input)
    count = count + 1
    total = total + number

    # Update minimum and maximum
    if minimum is None or number < minimum:
        minimum = number
    if maximum is None or number > maximum:
        maximum = number

    print(f"  Added {number} (running total: {total})")

# Display results
print("")
print("=" * 40)
print("FINAL STATISTICS:")
print("=" * 40)

if count > 0:
    average = total / count
    print(f"Numbers entered: {count}")
    print(f"Sum: {total}")
    print(f"Average: {average:.2f}")
    print(f"Minimum: {minimum}")
    print(f"Maximum: {maximum}")
else:
    print("No numbers were entered!")

print("=" * 40)
