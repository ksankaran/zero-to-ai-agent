# From: Zero to AI Agent, Chapter 4, Section 4.5
# set_patterns_ai.py - Essential set patterns for AI development

# Pattern 1: Duplicate Detection in Datasets
dataset = {
    "seen_ids": set(),
    "duplicates": [],
    "unique_data": []
}

# Sample data with duplicates
samples = [
    ("id_001", "data1"),
    ("id_002", "data2"),
    ("id_001", "data1_duplicate"),  # Duplicate!
    ("id_003", "data3"),
    ("id_002", "data2_duplicate"),  # Duplicate!
]

print("Processing dataset:")
for sample_id, data in samples:
    if sample_id in dataset["seen_ids"]:
        dataset["duplicates"].append((sample_id, data))
        print(f"  Duplicate detected: {sample_id}")
    else:
        dataset["seen_ids"].add(sample_id)
        dataset["unique_data"].append((sample_id, data))
        print(f"  Added unique sample: {sample_id}")

print(f"\nStatistics:")
print(f"  Total unique: {len(dataset['seen_ids'])}")
print(f"  Duplicates found: {len(dataset['duplicates'])}")

# Pattern 2: Feature Selection for ML
all_features = {"age", "income", "education", "location", "gender", "occupation"}
selected_features = set()
excluded_features = set()

# Select features
features_to_add = ["age", "income", "education", "invalid_feature"]
valid_features = set(features_to_add) & all_features
invalid_features = set(features_to_add) - all_features

if invalid_features:
    print(f"\nWarning: Invalid features ignored: {invalid_features}")

selected_features.update(valid_features)
print(f"Selected features: {selected_features}")

# Exclude features
excluded_features.add("gender")  # Remove for privacy
selected_features -= excluded_features

# Get unused features
unused_features = all_features - selected_features - excluded_features
print(f"Final features: {selected_features}")
print(f"Unused features: {unused_features}")

# Pattern 3: User Session Tracking
session_tracker = {
    "active_sessions": set(),
    "completed_sessions": set(),
    "all_users": set()
}

# Simulate user activity
actions = [
    ("start", "user1"),
    ("start", "user2"),
    ("start", "user3"),
    ("end", "user1"),
    ("start", "user1"),  # Returning user
    ("start", "user4"),
    ("end", "user2"),
]

print("\nSession tracking:")
for action, user_id in actions:
    if action == "start":
        if user_id in session_tracker["active_sessions"]:
            print(f"  {user_id} already has active session")
        else:
            session_tracker["active_sessions"].add(user_id)
            session_tracker["all_users"].add(user_id)
            print(f"  Session started for {user_id}")
    else:  # end
        if user_id not in session_tracker["active_sessions"]:
            print(f"  No active session for {user_id}")
        else:
            session_tracker["active_sessions"].remove(user_id)
            session_tracker["completed_sessions"].add(user_id)
            print(f"  Session ended for {user_id}")

# Calculate metrics
active_count = len(session_tracker["active_sessions"])
total_users = len(session_tracker["all_users"])
returning_users = len(session_tracker["completed_sessions"])
new_users = len(session_tracker["all_users"] - session_tracker["completed_sessions"])

print(f"\nSession Metrics:")
print(f"  Active now: {active_count}")
print(f"  Total users: {total_users}")
print(f"  Returning users: {returning_users}")
print(f"  New users: {new_users}")
print(f"  Active user IDs: {session_tracker['active_sessions']}")
