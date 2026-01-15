# From: Zero to AI Agent, Chapter 4, Section 4.3
# Exercise 2: Game State Snapshots

# Store player position as tuple
position = (5, 10)
print(f"Starting position: {position}")

# Save game snapshots
snapshots = []

# Simulate game turns
game_states = [
    (1, (5, 10), 100, 100),
    (2, (6, 10), 120, 95),
    (3, (6, 11), 150, 90),
    (4, (7, 11), 200, 85),
    (5, (7, 12), 180, 80)
]

for state in game_states:
    snapshots.append(state)  # Immutable snapshot
    print(f"Turn {state[0]}: Pos {state[1]}, Score {state[2]}, Health {state[3]}")

# Find snapshot with highest score
highest_score_snapshot = max(snapshots, key=lambda s: s[2])
print(f"Highest score at turn {highest_score_snapshot[0]}: {highest_score_snapshot[2]}")

# Return game statistics
total_turns = len(snapshots)
avg_score = sum(s[2] for s in snapshots) / len(snapshots)
final_health = snapshots[-1][3]

stats = (total_turns, avg_score, final_health)
print(f"Game Stats - Turns: {stats[0]}, Avg Score: {stats[1]:.1f}, Final Health: {stats[2]}")
