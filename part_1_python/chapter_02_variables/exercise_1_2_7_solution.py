# Exercise 1: Commented Recipe Calculator
# Add clear comments to a recipe scaling program

# Solution:

# ============================================
# Recipe Scaling Calculator
# This program scales a cookie recipe based on
# how many batches you want to make.
# ============================================

# Original recipe makes 24 cookies
# These are the base ingredient amounts
original_cookies = 24
flour_cups = 2.25        # All-purpose flour
sugar_cups = 0.75        # Granulated sugar
butter_cups = 1.0        # Softened butter
eggs = 2                 # Large eggs
vanilla_tsp = 1.0        # Vanilla extract

# How many cookies do we want to make?
desired_cookies = 72

# Calculate the scaling factor
# This tells us how many times to multiply each ingredient
scale_factor = desired_cookies / original_cookies

# Scale each ingredient by multiplying by the factor
scaled_flour = flour_cups * scale_factor
scaled_sugar = sugar_cups * scale_factor
scaled_butter = butter_cups * scale_factor
scaled_eggs = eggs * scale_factor
scaled_vanilla = vanilla_tsp * scale_factor

# Display the results with clear formatting
print("=" * 40)
print("COOKIE RECIPE SCALER")
print("=" * 40)

# Show the scaling information
print(f"\nOriginal recipe: {original_cookies} cookies")
print(f"Desired amount: {desired_cookies} cookies")
print(f"Scale factor: {scale_factor}x")

# Display scaled ingredients
print("\nScaled Ingredients:")
print("-" * 40)
print(f"Flour:   {scaled_flour:.2f} cups")
print(f"Sugar:   {scaled_sugar:.2f} cups")
print(f"Butter:  {scaled_butter:.2f} cups")
print(f"Eggs:    {scaled_eggs:.0f}")
print(f"Vanilla: {scaled_vanilla:.1f} tsp")
print("=" * 40)
