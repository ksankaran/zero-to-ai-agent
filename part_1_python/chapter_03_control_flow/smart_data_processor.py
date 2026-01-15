# From: Zero to AI Agent, Chapter 3, Section 3.6
# smart_data_processor.py
# Smart Data Processing Pipeline (without lists)

print("=" * 40)
print("SMART DATA PROCESSING PIPELINE")
print("=" * 40)
print("")
print("Enter data points (type 'done' to finish, 'skip' to skip a value):")

# Track running statistics instead of storing in a list
count = 0
total = 0
minimum = None
maximum = None

while True:
    user_input = input("Data point: ").lower().strip()

    if user_input == "done":
        break  # Exit the loop

    if user_input == "skip" or user_input == "":
        continue  # Skip to next iteration

    value = float(user_input)

    # Validate the data
    if value < 0:
        print("Negative values not allowed. Skipping...")
        continue

    if value > 1000:
        print("Value too large! Safety limit exceeded.")
        response = input("Override safety? (yes/no): ").lower()
        if response != "yes":
            continue

    # Update running statistics
    count = count + 1
    total = total + value

    if minimum is None or value < minimum:
        minimum = value
    if maximum is None or value > maximum:
        maximum = value

    print(f"Added: {value} (running total: {total})")

# Process the collected data
print("")
print("-" * 40)

if count == 0:
    print("No data to process!")
else:
    average = total / count
    print(f"Processing {count} data points...")
    print(f"Sum: {total}")
    print(f"Average: {average:.2f}")
    print(f"Maximum: {maximum}")
    print(f"Minimum: {minimum}")

print("=" * 40)
