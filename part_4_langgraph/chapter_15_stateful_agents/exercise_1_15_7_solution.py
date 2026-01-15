# From: Zero to AI Agent, Chapter 15, Section 15.7
# File: exercise_1_15_7_solution.py

"""
State diff viewer - compare snapshots and highlight changes.
"""

def diff_states(before: dict, after: dict) -> dict:
    """Compare two state snapshots."""
    diff = {
        "added": {},
        "removed": {},
        "modified": {},
        "unchanged": []
    }
    
    all_keys = set(before.keys()) | set(after.keys())
    
    for key in all_keys:
        if key not in before:
            diff["added"][key] = after[key]
        elif key not in after:
            diff["removed"][key] = before[key]
        elif before[key] != after[key]:
            diff["modified"][key] = {
                "from": before[key],
                "to": after[key]
            }
        else:
            diff["unchanged"].append(key)
    
    return diff

def print_diff(diff: dict, title: str = "State Diff"):
    """Format and print state diff."""
    print(f"\n{'═' * 50}")
    print(f"📊 {title}")
    print(f"{'═' * 50}")
    
    if diff["added"]:
        print("\n✅ Added:")
        for key, value in diff["added"].items():
            print(f"  + {key}: {value}")
    
    if diff["removed"]:
        print("\n❌ Removed:")
        for key, value in diff["removed"].items():
            print(f"  - {key}: {value}")
    
    if diff["modified"]:
        print("\n📝 Modified:")
        for key, change in diff["modified"].items():
            print(f"  ~ {key}:")
            print(f"      from: {change['from']}")
            print(f"      to:   {change['to']}")
    
    if diff["unchanged"]:
        print(f"\n⏸️ Unchanged: {', '.join(diff['unchanged'])}")
    
    # Summary
    total_changes = len(diff["added"]) + len(diff["removed"]) + len(diff["modified"])
    print(f"\n{'─' * 50}")
    print(f"Summary: {total_changes} change(s)")
    print(f"{'═' * 50}\n")

# Demo
if __name__ == "__main__":
    before = {
        "messages": ["Hello"],
        "count": 1,
        "status": "active",
        "user": "alice"
    }
    
    after = {
        "messages": ["Hello", "World"],
        "count": 2,
        "status": "active",
        "priority": "high"  # Added
        # "user" removed
    }
    
    diff = diff_states(before, after)
    print_diff(diff, "Step 1 → Step 2")
