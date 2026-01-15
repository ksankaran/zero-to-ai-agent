# From: Zero to AI Agent, Chapter 3, Section 3.1
# Exercise 2: AI Agent Mood Simulator
# AI assistant that responds differently based on the user's mood

print("=" * 40)
print("AI MOOD RESPONSE SYSTEM")
print("=" * 40)
print("I'm here to respond to how you're feeling!")
print("")

# Get the user's mood
mood = input("How are you feeling? (happy/sad/tired/excited/other): ").lower().strip()

# Respond based on mood
if mood == "happy":
    print("")
    print("That's wonderful! I'm so glad you're happy!")
    print("Here's a programming joke for you:")
    print("Why do programmers prefer dark mode?")
    print("Because light attracts bugs!")

elif mood == "sad":
    print("")
    print("I'm sorry you're feeling down.")
    print("Remember: Every expert was once a beginner.")
    print("Every master was once a disaster.")
    print("You're doing great, and tomorrow is a new day!")

elif mood == "tired":
    print("")
    print("Sounds like you need a break!")
    print("Here's what I suggest:")
    print("1. Step away from the computer for 10 minutes")
    print("2. Stretch your arms and legs")
    print("3. Grab some water or a healthy snack")
    print("4. Take a few deep breaths")
    print("Your brain needs rest to learn effectively!")

elif mood == "excited":
    print("")
    print("That's the spirit! Your enthusiasm is contagious!")
    print("Channel that energy into your coding!")
    print("When you're excited about learning, you learn faster.")
    print("You're going to build amazing things!")

else:
    print("")
    print(f"I see you're feeling '{mood}'.")
    print("That's totally valid! Whatever you're feeling right now,")
    print("remember that you've got this!")
    print("Every line of code you write is progress.")

print("=" * 40)
