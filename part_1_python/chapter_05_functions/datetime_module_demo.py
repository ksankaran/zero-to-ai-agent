# From: Zero to AI Agent, Chapter 5, Section 5.6
# File: datetime_module_demo.py

from datetime import datetime, date, timedelta

# Current date and time
now = datetime.now()
print(f"Right now: {now}")
print(f"Year: {now.year}, Month: {now.month}, Day: {now.day}")
print(f"Time: {now.hour}:{now.minute}:{now.second}")

# Just the date
today = date.today()
print(f"Today's date: {today}")

# Format dates nicely
formatted = now.strftime("%B %d, %Y at %I:%M %p")
print(f"Formatted: {formatted}")

# Date arithmetic
tomorrow = today + timedelta(days=1)
next_week = today + timedelta(weeks=1)
print(f"Tomorrow: {tomorrow}")
print(f"Next week: {next_week}")

# Calculate age
birthday = date(2000, 1, 15)  # January 15, 2000
age = today - birthday
print(f"Age in days: {age.days}")
print(f"Age in years: {age.days // 365}")