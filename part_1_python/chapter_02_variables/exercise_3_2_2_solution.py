# Exercise 3: Time Calculator
# Convert seconds into hours, minutes, and seconds format

# Solution:

# Starting value
total_seconds = 7439

# Calculate hours
hours = total_seconds // 3600  # 3600 seconds in an hour
remaining_seconds = total_seconds % 3600

# Calculate minutes from remaining seconds
minutes = remaining_seconds // 60  # 60 seconds in a minute
seconds = remaining_seconds % 60

# Display the result
print("Time Calculator")
print("-" * 30)
print("Total seconds:", total_seconds)
print(f"Converted: {hours} hours, {minutes} minutes, {seconds} seconds")

# Alternative display formats
print(f"\nFormatted: {hours:02d}:{minutes:02d}:{seconds:02d}")
print(f"Verbal: {hours} hour(s), {minutes} minute(s), and {seconds} second(s)")

# Show the calculation
print("\n--- Calculation breakdown ---")
print(f"Hours: {total_seconds} // 3600 = {hours}")
print(f"Remaining: {total_seconds} % 3600 = {remaining_seconds}")
print(f"Minutes: {remaining_seconds} // 60 = {minutes}")
print(f"Seconds: {remaining_seconds} % 60 = {seconds}")

# Test with a different value
print("\n--- Test with 3661 seconds ---")
test_seconds = 3661
test_hours = test_seconds // 3600
test_remaining = test_seconds % 3600
test_minutes = test_remaining // 60
test_secs = test_remaining % 60
print(f"{test_seconds} seconds = {test_hours}h {test_minutes}m {test_secs}s")
