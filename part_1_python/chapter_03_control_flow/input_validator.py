# From: Zero to AI Agent, Chapter 3, Section 3.5
# input_validator.py

print("🎮 Game Difficulty Selector\n")

difficulty = ""
while difficulty not in ["easy", "medium", "hard"]:
    print("Choose difficulty: easy, medium, or hard")
    difficulty = input("Your choice: ").lower()
    
    if difficulty not in ["easy", "medium", "hard"]:
        print("❌ Invalid choice! Please try again.\n")

print(f"\n✅ You selected: {difficulty.upper()}")
print("Loading game...")
