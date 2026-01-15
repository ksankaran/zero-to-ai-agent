# Exercise 2: Alien Age Calculator
# Calculate your age on different planets!

# Solution:

print("=" * 40)
print("ALIEN AGE CALCULATOR")
print("=" * 40)

# Your Earth age
earth_age = 25

# Planet year lengths (in Earth years)
# Mercury orbits the Sun in 0.24 Earth years
# Venus orbits in 0.62 Earth years
# Mars orbits in 1.88 Earth years
# Jupiter orbits in 11.86 Earth years
# Saturn orbits in 29.46 Earth years

mercury_age = earth_age / 0.24
venus_age = earth_age / 0.62
mars_age = earth_age / 1.88
jupiter_age = earth_age / 11.86
saturn_age = earth_age / 29.46

print(f"\nIf you are {earth_age} years old on Earth...")
print("")
print(f"On Mercury: {mercury_age:.1f} years old")
print(f"On Venus: {venus_age:.1f} years old")
print(f"On Mars: {mars_age:.1f} years old")
print(f"On Jupiter: {jupiter_age:.1f} years old")
print(f"On Saturn: {saturn_age:.1f} years old")

print("")
print("=" * 40)
print("Mercury spins fast - you'd be ancient!")
print("Jupiter is slow - you'd be a toddler!")
print("=" * 40)
