# From: Zero to AI Agent, Chapter 4, Section 4.3
# Exercise 1: Color Palette Manager
# Store and manipulate colors using tuples (without functions)

print("=" * 40)
print("COLOR PALETTE MANAGER")
print("=" * 40)

# Store RGB colors as tuples (immutable)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
print(f"Red: {red}")
print(f"Green: {green}")
print(f"Blue: {blue}")

# Mix two colors by averaging their RGB values
# Mixing red and blue to make purple
mixed_r = (red[0] + blue[0]) // 2
mixed_g = (red[1] + blue[1]) // 2
mixed_b = (red[2] + blue[2]) // 2
purple = (mixed_r, mixed_g, mixed_b)
print(f"\nMixed (red + blue): {purple}")

# Store colors with coordinate keys (tuples as dictionary keys)
color_map = {
    (0, 0): red,
    (1, 0): green,
    (0, 1): blue,
    (1, 1): purple
}
print(f"\nColor at position (1,1): {color_map[(1, 1)]}")

# Display all positions and their colors
print("\nAll colors in the map:")
for position, color in color_map.items():
    print(f"  Position {position}: RGB {color}")

# Convert RGB to hex format
# For red color
hex_red = '#' + format(red[0], '02x') + format(red[1], '02x') + format(red[2], '02x')
print(f"\nRed in hex format: {hex_red}")

# For purple color
hex_purple = '#' + format(purple[0], '02x') + format(purple[1], '02x') + format(purple[2], '02x')
print(f"Purple in hex format: {hex_purple}")

print("=" * 40)
