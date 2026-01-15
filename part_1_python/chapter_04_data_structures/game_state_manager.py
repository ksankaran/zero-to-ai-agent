# From: Zero to AI Agent, Chapter 4, Section 4.3
# game_state_manager.py - Using tuples for immutable game snapshots

# Game State Management System
# Using tuples for immutable snapshots and lists for history

# Initialize game
game_data = {
    "player_name": "Hero",
    "current_position": (0, 0),  # Starting position as tuple
    "current_stats": {
        "health": 100,
        "score": 0,
        "level": 1
    },
    "snapshots": [],  # Will store immutable snapshots
    "move_history": []  # Will store move records
}

print("Game initialized!")
print(f"Player: {game_data['player_name']}")
print(f"Starting position: {game_data['current_position']}")

# Simulate game moves
moves = [
    ("right", 1, 0, 10),   # (direction, dx, dy, points)
    ("up", 0, 1, 15),
    ("right", 1, 0, 20),
    ("down", 0, -1, -5),   # Lost points!
    ("left", -1, 0, 25)
]

print("\nPlaying game:")
for move_num, move_data in enumerate(moves, 1):
    direction, dx, dy, points = move_data
    
    # Update position (create new tuple)
    old_x, old_y = game_data["current_position"]
    new_position = (old_x + dx, old_y + dy)
    old_position = game_data["current_position"]
    game_data["current_position"] = new_position
    
    # Update score
    game_data["current_stats"]["score"] += points
    
    # Create immutable snapshot of this moment
    snapshot = (
        move_num,
        new_position,
        game_data["current_stats"]["score"],
        game_data["current_stats"]["health"],
        direction
    )
    game_data["snapshots"].append(snapshot)
    
    # Record the move
    move_record = (direction, old_position, new_position, points)
    game_data["move_history"].append(move_record)
    
    print(f"  Move {move_num}: {direction} to {new_position}, Score: {game_data['current_stats']['score']}")

# Analyze game history
print("\n=== Game Analysis ===")
print(f"Total moves: {len(game_data['snapshots'])}")
print(f"Final position: {game_data['current_position']}")
print(f"Final score: {game_data['current_stats']['score']}")

# Find best scoring move
if game_data["move_history"]:
    best_move = max(game_data["move_history"], key=lambda x: x[3])  # x[3] is points
    direction, from_pos, to_pos, points = best_move
    print(f"Best move: {direction} from {from_pos} to {to_pos} (+{points} points)")

# Show all snapshots
print("\n=== Game Snapshots ===")
for snapshot in game_data["snapshots"]:
    move, pos, score, health, direction = snapshot
    print(f"  After move {move}: Position {pos}, Score {score}, Health {health}")
