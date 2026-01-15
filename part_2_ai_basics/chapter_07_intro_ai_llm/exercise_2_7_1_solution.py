# From: Zero to AI Agent, Chapter 7, Section 7.1
# File: exercise_2_7_1_solution.py

"""
Exercise 2 Solution: Categorizing AI Types
Match AI applications to their learning type:
- Supervised Learning: Learns from labeled examples
- Unsupervised Learning: Finds patterns without labels
- Reinforcement Learning: Learns through trial and error with rewards
"""

def categorize_applications():
    """
    Categorizes AI applications by their learning type.
    Returns a list of applications with their classifications.
    """
    
    applications = [
        {
            "id": "A",
            "description": "An email filter trained on examples of spam and not-spam emails",
            "type": "Supervised Learning",
            "reason": "Has labeled examples (spam or not spam) to learn from"
        },
        {
            "id": "B",
            "description": "A system that groups customers by shopping behavior without predefined categories",
            "type": "Unsupervised Learning",
            "reason": "Finds natural groupings without being told what groups should exist"
        },
        {
            "id": "C",
            "description": "A robot learning to walk by trying different movements and getting points for distance traveled",
            "type": "Reinforcement Learning",
            "reason": "Gets rewards (distance) for good attempts, learns from success/failure"
        },
        {
            "id": "D",
            "description": "A model that predicts house prices from past sales data with known prices",
            "type": "Supervised Learning",
            "reason": "Learns from examples with known prices (labels)"
        },
        {
            "id": "E",
            "description": "An AI finding hidden patterns in genetic data without knowing what diseases to look for",
            "type": "Unsupervised Learning",
            "reason": "Discovers patterns without predefined disease categories"
        },
        {
            "id": "F",
            "description": "A game-playing AI that improves by winning/losing thousands of games",
            "type": "Reinforcement Learning",
            "reason": "Learns from rewards (winning) and penalties (losing)"
        },
        {
            "id": "G",
            "description": "A photo app that learned to identify faces after seeing millions of labeled face images",
            "type": "Supervised Learning",
            "reason": "Trained on millions of images labeled as 'face' or 'not face'"
        }
    ]
    
    return applications


def display_by_category():
    """Displays applications grouped by learning type."""
    
    print("="*70)
    print("EXERCISE 2 SOLUTION: Types of Machine Learning")
    print("="*70)
    
    applications = categorize_applications()
    
    # Group by type
    supervised = [app for app in applications if app["type"] == "Supervised Learning"]
    unsupervised = [app for app in applications if app["type"] == "Unsupervised Learning"]
    reinforcement = [app for app in applications if app["type"] == "Reinforcement Learning"]
    
    # Display Supervised Learning
    print("\n📚 SUPERVISED LEARNING (Learning with a teacher)")
    print("-" * 50)
    print("Pattern: Has labeled training data with correct answers")
    print("\nApplications:")
    for app in supervised:
        print(f"\n{app['id']}. {app['description']}")
        print(f"   Why: {app['reason']}")
    
    # Display Unsupervised Learning
    print("\n" + "="*70)
    print("🔍 UNSUPERVISED LEARNING (Finding patterns alone)")
    print("-" * 50)
    print("Pattern: No labels, discovers hidden structure in data")
    print("\nApplications:")
    for app in unsupervised:
        print(f"\n{app['id']}. {app['description']}")
        print(f"   Why: {app['reason']}")
    
    # Display Reinforcement Learning
    print("\n" + "="*70)
    print("🎮 REINFORCEMENT LEARNING (Learning by doing)")
    print("-" * 50)
    print("Pattern: Learns through trial and error with rewards/penalties")
    print("\nApplications:")
    for app in reinforcement:
        print(f"\n{app['id']}. {app['description']}")
        print(f"   Why: {app['reason']}")
    
    # Summary and quick reference
    print("\n" + "="*70)
    print("QUICK REFERENCE GUIDE")
    print("="*70)
    print("\n💡 How to identify each type:")
    print("\n1. SUPERVISED LEARNING:")
    print("   • Has training data with correct answers/labels")
    print("   • Examples: spam/not-spam, cat/dog, price predictions")
    print("   • Think: Learning with a teacher showing right answers")
    
    print("\n2. UNSUPERVISED LEARNING:")
    print("   • No labels, just raw data")
    print("   • Finds hidden patterns or groups")
    print("   • Examples: customer segmentation, anomaly detection")
    print("   • Think: Explorer finding patterns on their own")
    
    print("\n3. REINFORCEMENT LEARNING:")
    print("   • Learns by trying actions and getting feedback")
    print("   • Rewards for good actions, penalties for bad")
    print("   • Examples: game AI, robotics, trading bots")
    print("   • Think: Learning to ride a bike through practice")


def show_answer_key():
    """Shows a simple answer key format."""
    
    print("\n" + "="*70)
    print("ANSWER KEY (Quick Reference)")
    print("="*70)
    
    applications = categorize_applications()
    
    print("\nSupervised Learning: ", end="")
    supervised_ids = [app['id'] for app in applications if app['type'] == "Supervised Learning"]
    print(", ".join(supervised_ids))
    
    print("Unsupervised Learning: ", end="")
    unsupervised_ids = [app['id'] for app in applications if app['type'] == "Unsupervised Learning"]
    print(", ".join(unsupervised_ids))
    
    print("Reinforcement Learning: ", end="")
    reinforcement_ids = [app['id'] for app in applications if app['type'] == "Reinforcement Learning"]
    print(", ".join(reinforcement_ids))


if __name__ == "__main__":
    display_by_category()
    show_answer_key()
