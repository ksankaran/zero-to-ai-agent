# division_surprise.py
# From: Zero to AI Agent, Chapter 2, Section 2.2
# Division always returns a float in Python 3

result1 = 10 / 2   # You might expect 5 (integer)
print("10 / 2 =", result1)
print("Type:", type(result1))  # But it's 5.0 (float)!

result2 = 10 / 3
print("\n10 / 3 =", result2)   # 3.3333333333333335

# If you want an integer result, use floor division
result3 = 10 // 2
print("\n10 // 2 =", result3)
print("Type:", type(result3))  # Now it's an integer!

# Floor division always rounds DOWN
print("\n17 // 5 =", 17 // 5)    # 3 (not 3.4)
print("-17 // 5 =", -17 // 5)    # -4 (rounds down, so more negative!)
