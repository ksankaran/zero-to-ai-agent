# From: Zero to AI Agent, Chapter 3, Section 3.7
# ai_game_opponent.py

print("🎮 AI Game Opponent Decision System\n")

player_health = 100
ai_health = 100
turn = 0

while player_health > 0 and ai_health > 0:
    turn += 1
    print(f"\n--- Turn {turn} ---")
    print(f"Player Health: {player_health} | AI Health: {ai_health}")
    
    # Player's turn
    print("\nYour move: 1=Attack, 2=Defend, 3=Heal")
    player_move = int(input("Choose: "))
    
    # AI decision logic (nested conditions)
    ai_move = ""
    if ai_health < 30:
        # Low health - defensive strategy
        if player_health > 70:
            ai_move = "heal"  # Player is strong, need to heal
        else:
            ai_move = "defend"  # Both weak, play safe
    elif ai_health > 70:
        # High health - aggressive strategy
        if player_health < 50:
            ai_move = "attack"  # Player is weak, finish them!
        else:
            # Use pattern recognition
            if turn % 2 == 0:
                ai_move = "attack"
            else:
                ai_move = "defend"
    else:
        # Medium health - balanced strategy
        if player_move == 2:  # If player defending
            ai_move = "heal"
        else:
            ai_move = "attack"
    
    # Execute moves
    print(f"\nAI chooses to {ai_move}!")
    
    # Simple combat resolution
    if player_move == 1 and ai_move != "defend":
        ai_health -= 20
        print("You hit the AI!")
    if ai_move == "attack" and player_move != 2:
        player_health -= 15
        print("AI hits you!")
    if player_move == 3:
        player_health = min(100, player_health + 25)
        print("You healed!")
    if ai_move == "heal":
        ai_health = min(100, ai_health + 25)
        print("AI healed!")

# Game over
print("\n" + "=" * 30)
if player_health <= 0:
    print("❌ AI Wins! Better luck next time!")
else:
    print("🎉 You Win! Congratulations!")
