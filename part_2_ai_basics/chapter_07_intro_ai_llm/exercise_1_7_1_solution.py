# From: Zero to AI Agent, Chapter 7, Section 7.1
# File: exercise_1_7_1_solution.py

"""
Exercise 1 Solution: AI or Not AI?
Determine if each system uses AI or traditional programming.
"""

def analyze_systems():
    """
    Analyzes 10 systems to determine if they use AI or traditional programming.
    Key principle: If it adapts based on data or improves over time, it's probably AI!
    """
    
    systems = [
        {
            "number": 1,
            "name": "A calculator app that adds numbers",
            "answer": "Traditional Programming",
            "icon": "⚙️",
            "reason": "Follows fixed mathematical rules, no learning involved"
        },
        {
            "number": 2,
            "name": "Google Photos finding all pictures of your dog",
            "answer": "AI",
            "icon": "🤖",
            "reason": "Learned to recognize dogs (and specific dogs!) from millions of images"
        },
        {
            "number": 3,
            "name": "A website login that checks if password matches",
            "answer": "Traditional Programming",
            "icon": "⚙️",
            "reason": "Simple comparison: does input equal stored password?"
        },
        {
            "number": 4,
            "name": "Spotify creating your 'Discover Weekly' playlist",
            "answer": "AI",
            "icon": "🤖",
            "reason": "Learns your music taste from listening patterns"
        },
        {
            "number": 5,
            "name": "An alarm clock that rings at 7 AM",
            "answer": "Traditional Programming",
            "icon": "⚙️",
            "reason": "Fixed rule: if time = 7:00 AM, then ring"
        },
        {
            "number": 6,
            "name": "Your phone's face unlock",
            "answer": "AI",
            "icon": "🤖",
            "reason": "Learned to recognize faces, adapts to changes (glasses, beard, etc.)"
        },
        {
            "number": 7,
            "name": "A thermostat that turns on at 70°F",
            "answer": "Traditional Programming",
            "icon": "⚙️",
            "reason": "Simple rule: if temperature < 70°F, turn on heat"
        },
        {
            "number": 8,
            "name": "Gmail's spam filter",
            "answer": "AI",
            "icon": "🤖",
            "reason": "Learned patterns of spam from millions of emails"
        },
        {
            "number": 9,
            "name": "A video game where enemies always patrol the same path",
            "answer": "Traditional Programming",
            "icon": "⚙️",
            "reason": "Pre-programmed movement patterns"
        },
        {
            "number": 10,
            "name": "YouTube's recommendation algorithm",
            "answer": "AI",
            "icon": "🤖",
            "reason": "Learns what you like based on viewing history and similar users"
        }
    ]
    
    return systems


def print_results():
    """Displays the analysis results in a clear format."""
    
    print("="*60)
    print("EXERCISE 1 SOLUTION: AI or Traditional Programming?")
    print("="*60)
    
    systems = analyze_systems()
    
    # Count totals
    ai_count = sum(1 for s in systems if s["answer"] == "AI")
    traditional_count = len(systems) - ai_count
    
    # Display each system
    for system in systems:
        print(f"\n{system['number']}. {system['name']}")
        print(f"   Answer: {system['icon']} {system['answer']}")
        print(f"   Why: {system['reason']}")
    
    # Summary
    print("\n" + "-"*60)
    print(f"SUMMARY: {ai_count} AI systems, {traditional_count} Traditional Programming systems")
    print("\n💡 Quick Rule: If it adapts based on data or improves over time, it's probably AI!")
    
    # Additional insights
    print("\n" + "="*60)
    print("KEY PATTERNS TO REMEMBER:")
    print("="*60)
    print("\n✅ Signs of AI:")
    print("  • Learns from examples")
    print("  • Improves over time")
    print("  • Recognizes patterns")
    print("  • Makes predictions")
    print("  • Adapts to user behavior")
    
    print("\n⚙️ Signs of Traditional Programming:")
    print("  • Follows fixed rules")
    print("  • Same output for same input")
    print("  • No learning involved")
    print("  • Simple if-then logic")
    print("  • Doesn't improve with use")


if __name__ == "__main__":
    print_results()
