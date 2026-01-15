# From: Zero to AI Agent, Chapter 4, Section 4.5
# Exercise 1: Email List Manager

# Manage email lists
campaigns = {
    "newsletter": {"alice@example.com", "bob@example.com", "charlie@example.com"},
    "promo": {"bob@example.com", "diana@example.com", "charlie@example.com"},
    "updates": {"alice@example.com", "diana@example.com", "eve@example.com"}
}

# Add emails (no duplicates)
campaigns["newsletter"].add("frank@example.com")
campaigns["newsletter"].add("alice@example.com")  # Already exists
print(f"Newsletter subscribers: {campaigns['newsletter']}")

# Find common subscribers
common = campaigns["newsletter"] & campaigns["promo"]
print(f"\nCommon between newsletter and promo: {common}")

# Exclusive subscribers
newsletter_only = campaigns["newsletter"] - campaigns["promo"]
print(f"Newsletter only: {newsletter_only}")

# Merge lists without duplicates
all_subscribers = campaigns["newsletter"] | campaigns["promo"] | campaigns["updates"]
print(f"\nAll unique subscribers: {len(all_subscribers)}")

# Statistics
print("\nCampaign Overlap Statistics:")
for c1 in campaigns:
    for c2 in campaigns:
        if c1 < c2:  # Avoid duplicate comparisons
            overlap = len(campaigns[c1] & campaigns[c2])
            print(f"  {c1} & {c2}: {overlap} common subscribers")
