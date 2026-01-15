# logical_operators.py
# From: Zero to AI Agent, Chapter 2, Section 2.4
# Combining multiple conditions with and, or, not

# AND: Both conditions must be True
age = 25
has_license = True
can_drive = age >= 16 and has_license
print("=== AND Logic ===")
print(f"Age: {age}, Has license: {has_license}")
print(f"Can drive (age >= 16 AND has_license)? {can_drive}")

# More AND examples
temperature = 72
humidity = 45
nice_weather = temperature >= 70 and temperature <= 80 and humidity < 60
print(f"\nTemperature: {temperature}, Humidity: {humidity}")
print(f"Nice weather? {nice_weather}")

# OR: At least one condition must be True
print("\n=== OR Logic ===")
is_weekend = True
is_holiday = False
can_sleep_in = is_weekend or is_holiday
print(f"Weekend: {is_weekend}, Holiday: {is_holiday}")
print(f"Can sleep in? {can_sleep_in}")

# More OR examples
has_cash = False
has_credit_card = True
has_phone_pay = True
can_pay = has_cash or has_credit_card or has_phone_pay
print(f"\nPayment methods - Cash: {has_cash}, Card: {has_credit_card}, Phone: {has_phone_pay}")
print(f"Can pay for lunch? {can_pay}")

# NOT: Reverses the boolean
print("\n=== NOT Logic ===")
is_busy = False
is_available = not is_busy
print(f"Busy: {is_busy}")
print(f"Available: {is_available}")

# Combining all three
age = 19
is_student = True
has_student_id = True
# Student discount: Must be a student with ID, OR under 18
gets_student_discount = (is_student and has_student_id) or (age < 18)
print(f"\n=== Complex Condition ===")
print(f"Age: {age}, Student: {is_student}, Has ID: {has_student_id}")
print(f"Gets student discount? {gets_student_discount}")
