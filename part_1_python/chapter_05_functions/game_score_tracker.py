# From: Zero to AI Agent, Chapter 5, Section 5.4
# File: game_score_tracker.py

# Good use of a global constant
DEFAULT_STARTING_SCORE = 100

def create_player(name):
    """Create a new player with starting score"""
    return {
        "name": name,
        "score": DEFAULT_STARTING_SCORE,
        "achievements": []
    }

def add_achievement(player, achievement, points):
    """Add achievement and update score (returns updated player)"""
    player["achievements"].append(achievement)
    player["score"] += points
    return player

def get_player_status(player):
    """Get formatted status (returns string)"""
    status = f"""
    Player: {player['name']}
    Score: {player['score']}
    Achievements: {', '.join(player['achievements']) if player['achievements'] else 'None yet'}
    """
    return status

def play_game():
    """Main game function - keeps everything local"""
    # Create local player data
    player1 = create_player("Alice")
    
    # Game events (modifying and returning)
    player1 = add_achievement(player1, "First Steps", 10)
    player1 = add_achievement(player1, "Found Treasure", 50)
    player1 = add_achievement(player1, "Defeated Boss", 100)
    
    # Get and display status
    status = get_player_status(player1)
    print(status)
    
    # Return final player data so it can be used elsewhere
    return player1

# Run the game and get the result
final_player = play_game()
print(f"Final score: {final_player['score']}")