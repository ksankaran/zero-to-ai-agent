# From: Zero to AI Agent, Chapter 3, Section 3.4
# ai_training_simulator.py

print("🧠 Neural Network Training Simulator\n")

epochs = int(input("Number of training epochs: "))
samples_per_epoch = int(input("Samples per epoch: "))

accuracy = 10.0  # Starting accuracy

for epoch in range(1, epochs + 1):
    print(f"\n--- Epoch {epoch} ---")
    
    # Simulate processing each sample in this epoch
    improvements = 0
    for sample in range(1, samples_per_epoch + 1):
        # Simulate learning (in real AI, this would be complex math!)
        if sample % 3 == 0:  # Every third sample improves accuracy
            improvements += 1
    
    # Update accuracy based on learning
    accuracy += improvements * 2.5
    if accuracy > 95:
        accuracy = 95 + (accuracy - 95) * 0.1  # Diminishing returns
    
    print(f"Samples processed: {samples_per_epoch}")
    print(f"Improvements made: {improvements}")
    print(f"Current accuracy: {accuracy:.1f}%")
    
    # Early stopping if we're doing well
    if accuracy >= 95:
        print("\n🎯 Target accuracy reached! Training complete.")
        break

print(f"\n📈 Final Model Accuracy: {accuracy:.1f}%")
