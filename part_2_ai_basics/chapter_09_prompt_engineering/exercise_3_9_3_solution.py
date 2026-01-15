# From: Zero to AI Agent, Chapter 9, Section 9.3
# File: exercise_3_9_3_solution.py

"""
Customer support ticket classifier using few-shot learning
"""

support_classifier_prompt = """
Classify customer support tickets:

Ticket: "The app crashes when I try to upload photos larger than 10MB"
Category: Bug Report

Ticket: "Getting an error message: 'Invalid file format' when using .png files"
Category: Bug Report

Ticket: "Could you add a dark mode option to the mobile app?"
Category: Feature Request

Ticket: "It would be great if we could export reports as PDF files"
Category: Feature Request

Ticket: "I was charged twice for my subscription this month"
Category: Billing Issue

Ticket: "Why hasn't my refund been processed yet? It's been 2 weeks"
Category: Billing Issue

Ticket: "What's the difference between the Pro and Enterprise plans?"
Category: General Question

Ticket: "How do I reset my password?"
Category: General Question

Now classify this ticket:
Ticket: "{}"
Category:"""

def test_classifier():
    """Test the classifier with various tickets"""
    
    test_tickets = [
        # Clear cases
        ("The login button doesn't work on Safari browser", "Bug Report"),
        ("Can you add integration with Google Calendar?", "Feature Request"),
        ("I need a receipt for my last payment", "Billing Issue"),
        ("What are your business hours?", "General Question"),
        
        # Edge case - combines bug and billing
        ("The payment failed but you still charged me, and now the app won't let me access premium features", 
         "Billing Issue (primary) + Bug Report (secondary)"),
    ]
    
    print("CUSTOMER SUPPORT TICKET CLASSIFIER")
    print("="*50)
    print("Trained with 2 examples per category (8 total examples)")
    print("="*50)
    
    for ticket, expected in test_tickets:
        print(f"\nTicket: '{ticket[:60]}{'...' if len(ticket) > 60 else ''}'")
        print(f"Expected: {expected}")
        
        # Simulate classification
        if "crash" in ticket.lower() or "doesn't work" in ticket.lower() or "error" in ticket.lower():
            predicted = "Bug Report"
        elif "add" in ticket.lower() or "could you" in ticket.lower() or "would be great" in ticket.lower():
            predicted = "Feature Request"
        elif "charged" in ticket.lower() or "payment" in ticket.lower() or "refund" in ticket.lower() or "receipt" in ticket.lower():
            predicted = "Billing Issue"
        else:
            predicted = "General Question"
            
        print(f"Classified as: {predicted}")
        
        if "combines" in expected.lower():
            print("Note: This is a complex ticket that spans multiple categories")

def show_prompt_structure():
    """Display the full few-shot prompt structure"""
    
    print("\n" + "="*50)
    print("FEW-SHOT PROMPT STRUCTURE")
    print("="*50)
    print("\nThe prompt contains:")
    print("- 2 Bug Report examples")
    print("- 2 Feature Request examples")
    print("- 2 Billing Issue examples")
    print("- 2 General Question examples")
    print("\nPattern learned from examples:")
    print("- Bug Report: errors, crashes, things not working")
    print("- Feature Request: suggestions, 'could you', 'would be nice'")
    print("- Billing Issue: payments, charges, refunds, receipts")
    print("- General Question: how-to, information seeking")

if __name__ == "__main__":
    test_classifier()
    show_prompt_structure()
    
    print("\n" + "="*50)
    print("KEY INSIGHTS:")
    print("- Just 2 examples per category teaches the pattern")
    print("- AI generalizes to new vocabulary and phrasings")
    print("- Edge cases may need special handling or human review")