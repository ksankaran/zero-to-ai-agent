# From: Zero to AI Agent, Chapter 6, Section 6.1
# File: large_files.py

# First, let's create a "large" file (simulated)
print("Creating a simulated large file...")
with open("large_log.txt", "w") as f:
    for i in range(10000):
        f.write(f"Log entry {i}: Something happened at {i*5} seconds\n")
print("Created file with 10,000 lines")

# BAD: Loading everything into memory
# content = open("large_log.txt").read()  # Could crash with huge files!

# GOOD: Processing line by line
print("\nProcessing file efficiently:")
error_count = 0
warning_count = 0

with open("large_log.txt", "r") as file:
    for line_number, line in enumerate(file, 1):
        # Process each line individually
        if "999" in line:  # Simulating error detection
            error_count += 1
        if "500" in line:  # Simulating warning detection
            warning_count += 1
        
        # Show progress every 1000 lines
        if line_number % 1000 == 0:
            print(f"  Processed {line_number:,} lines...")

print(f"\nAnalysis complete!")
print(f"Lines with '999': {error_count}")
print(f"Lines with '500': {warning_count}")

# Reading in chunks for binary operations
print("\nReading file in chunks:")
chunk_size = 1024  # 1KB chunks

with open("large_log.txt", "r") as file:
    chunk_count = 0
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        chunk_count += 1
    print(f"File read in {chunk_count} chunks of {chunk_size} bytes")
