# From: Zero to AI Agent, Chapter 3, Section 3.7
# image_processor_simulator.py

print("📷 Image Brightness Grid Simulator")
print("Creating a 5x5 pixel 'image'...\n")

width = 5
height = 5

# Display a simple brightness grid
print("Original brightness values:")
for row in range(height):
    for col in range(width):
        # Create a gradient effect
        brightness = (row + col) * 10
        print(f"{brightness:3}", end=" ")
    print()  # New line after each row

print("\nApplying brightness filter...")
threshold = int(input("Enter brightness threshold (0-80): "))

print("\nFiltered image (■ = bright, □ = dim):")
for row in range(height):
    for col in range(width):
        brightness = (row + col) * 10
        if brightness > threshold:
            print("■", end=" ")
        else:
            print("□", end=" ")
    print()
