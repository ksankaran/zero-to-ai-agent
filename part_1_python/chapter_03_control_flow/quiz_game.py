# From: Zero to AI Agent, Chapter 3, Section 3.5
# quiz_game.py

import random

print("🧠 Math Quiz Game\n")

play_again = "yes"
total_score = 0
games_played = 0

while play_again == "yes":
    games_played += 1
    print(f"\n--- Game {games_played} ---")
    
    score = 0
    num_questions = 3
    
    for question in range(1, num_questions + 1):
        # Generate simple math questions
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        correct_answer = a + b
        
        user_answer = int(input(f"Question {question}: {a} + {b} = "))
        
        if user_answer == correct_answer:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong. The answer was {correct_answer}")
    
    print(f"\nGame Score: {score}/{num_questions}")
    total_score += score
    
    play_again = input("\nPlay again? (yes/no): ").lower()

print(f"\n📊 Final Statistics:")
print(f"Games played: {games_played}")
print(f"Total score: {total_score}")
print(f"Average score: {total_score/games_played:.1f}")
