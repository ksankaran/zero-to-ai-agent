# From: Zero to AI Agent, Chapter 4, Section 4.3
# tuple_patterns.py - Common tuple patterns in AI development

# Pattern 1: Batch processing with coordinates
training_data = [
    ((0, 0), "origin"),
    ((1, 0), "right"),
    ((0, 1), "up"),
    ((-1, 0), "left")
]

print("Training data:")
for coordinates, label in training_data:
    x, y = coordinates  # Unpack the tuple
    print(f"  Point at ({x}, {y}) is labeled '{label}'")

# Pattern 2: Multiple return values for model evaluation
# Simulate model evaluation
accuracy = 0.92
loss = 0.08
epochs_completed = 100
training_time = 45.3

# Return as tuple
evaluation_results = (accuracy, loss, epochs_completed, training_time)

# Clean unpacking
acc, loss_val, epochs, time_taken = evaluation_results
print(f"\nTraining complete: {acc:.2%} accuracy in {time_taken:.1f} seconds")

# Pattern 3: Configuration management
MODEL_CONFIGS = {
    "small": (32, 4, 512, 0.1),    # (batch_size, layers, hidden_dim, dropout)
    "medium": (64, 8, 1024, 0.2),
    "large": (128, 12, 2048, 0.3)
}

selected_config = MODEL_CONFIGS["medium"]
batch, layers, hidden, dropout = selected_config
print(f"\nMedium model: {layers} layers, {hidden} hidden dimensions")

# Pattern 4: Storing immutable state snapshots
# Training history - each snapshot is immutable
training_history = []

# Simulate training epochs
epoch_data = [
    (1, 0.5, 0.75),  # (epoch, loss, accuracy)
    (2, 0.3, 0.85),
    (3, 0.2, 0.90)
]

for epoch, loss, acc in epoch_data:
    # Each snapshot is an immutable tuple
    snapshot = (epoch, loss, acc)
    training_history.append(snapshot)

print("\nTraining History:")
for epoch, loss, acc in training_history:
    print(f"  Epoch {epoch}: loss={loss:.2f}, accuracy={acc:.2%}")

# Find best epoch (highest accuracy)
if training_history:
    best_epoch = max(training_history, key=lambda x: x[2])  # x[2] is accuracy
    epoch, loss, acc = best_epoch
    print(f"\nBest epoch: {epoch} with {acc:.2%} accuracy")
