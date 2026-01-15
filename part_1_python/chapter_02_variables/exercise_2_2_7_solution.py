# Exercise 2: Self-Documenting Code
# Improve cryptic variable names to be self-documenting

# Original cryptic code:
# d = 86400
# h = d / 3600
# m = (d % 3600) / 60

# Solution with self-documenting names:

# Time conversion constants
SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 3600
SECONDS_PER_DAY = 86400

# Convert one day to different time units
total_seconds_in_day = SECONDS_PER_DAY
hours_in_day = total_seconds_in_day / SECONDS_PER_HOUR
minutes_in_day = total_seconds_in_day / SECONDS_PER_MINUTE

# Display time conversions
print("Time Unit Conversions")
print("=" * 40)
print(f"1 day contains:")
print(f"  {total_seconds_in_day:,} seconds")
print(f"  {minutes_in_day:,.0f} minutes")
print(f"  {hours_in_day:.0f} hours")

# Example: Convert specific duration
duration_in_seconds = 7439
duration_hours = duration_in_seconds // SECONDS_PER_HOUR
remaining_seconds = duration_in_seconds % SECONDS_PER_HOUR
duration_minutes = remaining_seconds // SECONDS_PER_MINUTE
duration_seconds = remaining_seconds % SECONDS_PER_MINUTE

print(f"\n{duration_in_seconds} seconds equals:")
print(f"  {duration_hours} hours, {duration_minutes} minutes, {duration_seconds} seconds")
