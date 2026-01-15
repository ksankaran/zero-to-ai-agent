# Exercise 3: Savings Goal Calculator
# A well-documented program for calculating savings goals

# Solution:

# ============================================
# SAVINGS GOAL CALCULATOR
# ============================================
# This program helps you figure out how long
# it will take to reach a savings goal, and
# shows your progress along the way.
# ============================================

# ----- USER'S FINANCIAL INFORMATION -----
# Current amount saved (starting point)
current_savings = 2500.00

# Target savings goal
savings_goal = 10000.00

# How much can be saved each month
monthly_contribution = 500.00

# Expected annual interest rate (as decimal)
# 4% = 0.04
annual_interest_rate = 0.04

# ----- CALCULATIONS -----

# How much more do we need to save?
amount_remaining = savings_goal - current_savings

# Simple calculation: months without interest
months_needed_simple = amount_remaining / monthly_contribution

# Monthly interest rate (annual / 12)
monthly_interest_rate = annual_interest_rate / 12

# Progress percentage
progress_percent = (current_savings / savings_goal) * 100

# After one year of contributions (simple)
yearly_contribution = monthly_contribution * 12
balance_after_year = current_savings + yearly_contribution

# Interest earned on current savings (one year)
interest_first_year = current_savings * annual_interest_rate

# ----- DISPLAY RESULTS -----

print("=" * 45)
print("SAVINGS GOAL CALCULATOR".center(45))
print("=" * 45)

# Show current status
print("\nCurrent Status:")
print(f"  Current savings:    ${current_savings:>10,.2f}")
print(f"  Savings goal:       ${savings_goal:>10,.2f}")
print(f"  Amount remaining:   ${amount_remaining:>10,.2f}")
print(f"  Progress:           {progress_percent:>10.1f}%")

# Show plan details
print("\nSavings Plan:")
print(f"  Monthly contribution: ${monthly_contribution:>8,.2f}")
print(f"  Interest rate:        {annual_interest_rate:>8.1%}")

# Show projections
print("\nProjections (without compound interest):")
print(f"  Months to goal:       {months_needed_simple:>8.1f}")
print(f"  Years to goal:        {months_needed_simple/12:>8.1f}")

print("\nAfter 1 Year:")
print(f"  From contributions:   ${yearly_contribution:>8,.2f}")
print(f"  Interest earned:      ${interest_first_year:>8,.2f}")
print(f"  Projected balance:    ${balance_after_year + interest_first_year:>8,.2f}")

print("=" * 45)
