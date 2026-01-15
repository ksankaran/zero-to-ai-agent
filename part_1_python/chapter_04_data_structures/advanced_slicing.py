# From: Zero to AI Agent, Chapter 4, Section 4.1
# advanced_slicing.py - Advanced slicing patterns for AI/ML

# Simulating a dataset for machine learning
dataset = list(range(100))  # 0 to 99, imagine these are data samples

# Common AI/ML slicing patterns

# 1. Getting batches of data
batch_size = 10
first_batch = dataset[:batch_size]
second_batch = dataset[batch_size:batch_size*2]
print(f"First batch: {first_batch}")
print(f"Second batch: {second_batch}")

# 2. Train/test split (very common in ML!)
split_point = int(len(dataset) * 0.8)  # 80% for training
training_data = dataset[:split_point]   # First 80%
test_data = dataset[split_point:]       # Last 20%
print(f"Training samples: {len(training_data)}")
print(f"Test samples: {len(test_data)}")

# 3. Getting the last n items (like recent chat history)
recent_history = dataset[-5:]  # Last 5 items
print(f"Recent items: {recent_history}")

# 4. Skipping header/footer (common with data files)
data_with_header = ["HEADER", 10, 20, 30, 40, "FOOTER"]
clean_data = data_with_header[1:-1]  # Skip first and last
print(f"Clean data: {clean_data}")

# 5. Reverse order (useful for backpropagation in neural networks!)
forwards = [1, 2, 3, 4, 5]
backwards = forwards[::-1]
print(f"Forward: {forwards}")
print(f"Backward: {backwards}")
