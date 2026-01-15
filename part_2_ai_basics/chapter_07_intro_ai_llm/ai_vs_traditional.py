# From: Zero to AI Agent, Chapter 7, Section 7.1
# File: ai_vs_traditional.py

"""
Demonstrates the difference between traditional programming and AI approaches
to spam detection.
"""

# Traditional Programming: You define the rules
def is_spam_traditional(email):
    """
    Traditional approach to spam detection using predefined rules.
    You explicitly program what words indicate spam.
    """
    spam_words = ['winner', 'free', 'click here', 'urgent']
    for word in spam_words:
        if word.lower() in email.lower():
            return True
    return False


# AI Approach: The system learns the patterns
# (This is a conceptual example - we'll build real AI models in later chapters!)
def is_spam_ai(email, ai_model=None):
    """
    AI approach to spam detection using a trained model.
    The model learns patterns from thousands of examples.
    
    Note: This is a simplified example. In real applications,
    the model would be loaded from a trained neural network or
    machine learning model.
    """
    if ai_model is None:
        # Placeholder for when we don't have a real model yet
        # In practice, you'd load a trained model here
        return 0.5  # Return neutral probability
    
    # An AI model would have learned from thousands of examples
    # what makes an email spam, finding patterns we might miss
    probability = ai_model.predict(email)  # Returns 0.0 to 1.0
    return probability > 0.5


# Example usage
if __name__ == "__main__":
    test_emails = [
        "Congratulations! You're a WINNER! Click here for your FREE prize!",
        "Meeting rescheduled to 3 PM tomorrow",
        "URGENT: Your account needs verification",
        "Can you review the attached proposal?",
    ]
    
    print("Traditional Programming Approach:")
    print("-" * 40)
    for email in test_emails:
        result = is_spam_traditional(email)
        print(f"Email: {email[:50]}...")
        print(f"Spam: {result}\n")
    
    print("\nAI Approach (conceptual):")
    print("-" * 40)
    print("With a trained AI model, the system would analyze:")
    print("- Writing style patterns")
    print("- Sender reputation")
    print("- Context and semantics")
    print("- Thousands of subtle features humans might miss")
    print("\nResult: Much more accurate spam detection!")
