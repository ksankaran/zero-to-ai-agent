# practical_math.py
# From: Zero to AI Agent, Chapter 2, Section 2.2
# Real-world math problems

# Problem 1: Calculate a tip at a restaurant
bill_amount = 48.50
tip_percentage = 0.20  # 20%
tip_amount = bill_amount * tip_percentage
total_with_tip = bill_amount + tip_amount

print("Restaurant Bill Calculator")
print("-" * 30)
print(f"Bill: ${bill_amount}")
print(f"Tip (20%): ${tip_amount:.2f}")  # .2f means 2 decimal places
print(f"Total: ${total_with_tip:.2f}")

# Problem 2: Convert temperature
celsius = 25
fahrenheit = celsius * 9/5 + 32
print(f"\n{celsius}°C = {fahrenheit}°F")

# Problem 3: Calculate compound interest
principal = 1000  # Starting amount
rate = 0.05      # 5% annual interest
years = 3
amount = principal * (1 + rate) ** years
interest_earned = amount - principal

print(f"\nCompound Interest Calculator")
print("-" * 30)
print(f"Starting amount: ${principal}")
print(f"Interest rate: {rate * 100}%")
print(f"Years: {years}")
print(f"Final amount: ${amount:.2f}")
print(f"Interest earned: ${interest_earned:.2f}")

# Problem 4: Split a bill among friends
total_bill = 127.45
number_of_friends = 5
amount_per_person = total_bill / number_of_friends

print(f"\nBill Splitter")
print("-" * 30)
print(f"Total bill: ${total_bill}")
print(f"Number of people: {number_of_friends}")
print(f"Each person pays: ${amount_per_person:.2f}")
