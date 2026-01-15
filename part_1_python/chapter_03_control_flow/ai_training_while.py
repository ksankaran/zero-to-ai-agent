# From: Zero to AI Agent, Chapter 3, Section 3.5
# ai_training_while.py
# Simulating how AI learns and improves

print("🎯 AI Training Simulator")
print("Training the AI until it reaches 95% accuracy...\n")

accuracy = 50.0  # Starting accuracy (50%)
training_round = 0

while accuracy < 95:
    training_round += 1
    
    # Simulate the AI learning (getting better each round)
    improvement = 10 - (training_round * 0.5)  # Improvements get smaller over time
    
    # Make sure improvement doesn't go negative
    if improvement < 0.5:
        improvement = 0.5
    
    accuracy += improvement
    
    # Don't exceed 100%
    if accuracy > 100:
        accuracy = 100
    
    print(f"Round {training_round}: Accuracy = {accuracy:.1f}%")
    
    # Safety limit - stop if taking too long
    if training_round >= 20:
        print("\n⏱️ Reached maximum training rounds.")
        break

print(f"\n✅ Training complete!")
print(f"Final accuracy: {accuracy:.1f}%")
print(f"Training rounds needed: {training_round}")

if accuracy >= 95:
    print("🎉 Success! The AI is ready to use!")
else:
    print("📊 More training data needed for better results.")
