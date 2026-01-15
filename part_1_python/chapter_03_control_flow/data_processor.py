# From: Zero to AI Agent, Chapter 3, Section 3.4
# data_processor.py
# Simulating how AI processes training data

print("AI Training Data Processor 🤖")
number_of_samples = int(input("How many data samples to process? "))

total = 0
highest = float('-inf')  # Negative infinity (smallest possible number)
lowest = float('inf')    # Positive infinity (largest possible number)

for i in range(number_of_samples):
    value = float(input(f"Enter sample {i + 1}: "))
    
    # Update statistics
    total += value
    if value > highest:
        highest = value
    if value < lowest:
        lowest = value

# Calculate results
average = total / number_of_samples

print(f"\n📊 Data Analysis Complete!")
print(f"Samples processed: {number_of_samples}")
print(f"Average value: {average:.2f}")
print(f"Highest value: {highest}")
print(f"Lowest value: {lowest}")
print(f"Range: {highest - lowest}")
