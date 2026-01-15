# From: Building AI Agents, Chapter 14, Section 14.6
# File: exercise_1_14_6_solution.py

"""Email classifier with multi-way routing.

Exercise 1 Solution: Build a graph that classifies incoming emails
and routes them to specialized handlers (5 categories).
"""

import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


# === STATE ===

class EmailState(TypedDict):
    email_subject: str        # Subject line
    email_body: str           # Full email content
    sender: str               # Who sent it
    category: str             # Classification result
    action_taken: str         # What we did with it
    extracted_info: dict      # Any info we pulled out


# === CLASSIFICATION NODE ===

def classify_email(state: EmailState) -> dict:
    """Classify the email into one of 5 categories.
    
    Uses the subject, body, and sender to determine the type.
    """
    subject = state["email_subject"]
    body = state["email_body"]
    sender = state["sender"]
    
    prompt = f"""Classify this email into exactly ONE category:

    From: {sender}
    Subject: {subject}
    Body: {body}

    Categories:
    - URGENT: Time-sensitive, needs immediate response, emergencies
    - MEETING: Calendar invites, scheduling, meeting requests
    - NEWSLETTER: Marketing, promotions, subscriptions
    - PERSONAL: From friends, family, personal contacts
    - SPAM: Unwanted, suspicious, phishing attempts

    Respond with only the category name."""
    
    response = llm.invoke(prompt)
    category = response.content.strip().upper()
    
    # Validate - default to NEWSLETTER if unrecognized
    valid = ["URGENT", "MEETING", "NEWSLETTER", "PERSONAL", "SPAM"]
    if category not in valid:
        category = "NEWSLETTER"
    
    print(f"📧 Classified as: {category}")
    return {"category": category}


# === ROUTING FUNCTION ===

def route_email(state: EmailState) -> str:
    """Route to the appropriate handler based on category."""
    category = state["category"]
    return f"handle_{category.lower()}"


# === HANDLER NODES ===

def handle_urgent(state: EmailState) -> dict:
    """Generate quick acknowledgment for urgent emails."""
    prompt = f"""Write a brief acknowledgment for this urgent email.
    From: {state['sender']}
    Subject: {state['email_subject']}
    
    Acknowledge receipt and promise quick response (2-3 sentences)."""
    
    response = llm.invoke(prompt)
    print("🚨 Urgent: Acknowledgment generated")
    
    return {
        "action_taken": "ACKNOWLEDGED",
        "extracted_info": {"response_draft": response.content}
    }


def handle_meeting(state: EmailState) -> dict:
    """Extract meeting details from the email."""
    prompt = f"""Extract meeting information from this email:
    Subject: {state['email_subject']}
    Body: {state['email_body']}
    
    Extract: date/time, participants, location/link, purpose.
    Format as a brief summary."""
    
    response = llm.invoke(prompt)
    print("📅 Meeting: Details extracted")
    
    return {
        "action_taken": "MEETING_EXTRACTED",
        "extracted_info": {"meeting_details": response.content}
    }


def handle_newsletter(state: EmailState) -> dict:
    """Archive newsletter emails."""
    print("📰 Newsletter: Archived")
    return {
        "action_taken": "ARCHIVED",
        "extracted_info": {"folder": "Newsletters", "source": state["sender"]}
    }


def handle_personal(state: EmailState) -> dict:
    """Flag personal emails for review."""
    print("👤 Personal: Flagged for review")
    return {
        "action_taken": "FLAGGED_PERSONAL",
        "extracted_info": {"flag": "Needs your attention"}
    }


def handle_spam(state: EmailState) -> dict:
    """Delete spam emails."""
    print("🗑️ Spam: Deleted")
    return {
        "action_taken": "DELETED",
        "extracted_info": {"blocked_sender": state["sender"]}
    }


# === GRAPH BUILDER ===

def create_email_graph():
    """Build the email classifier graph with 5-way routing."""
    graph = StateGraph(EmailState)
    
    # Add nodes
    graph.add_node("classify", classify_email)
    graph.add_node("handle_urgent", handle_urgent)
    graph.add_node("handle_meeting", handle_meeting)
    graph.add_node("handle_newsletter", handle_newsletter)
    graph.add_node("handle_personal", handle_personal)
    graph.add_node("handle_spam", handle_spam)
    
    # Entry and routing
    graph.set_entry_point("classify")
    
    graph.add_conditional_edges(
        "classify",
        route_email,
        {
            "handle_urgent": "handle_urgent",
            "handle_meeting": "handle_meeting",
            "handle_newsletter": "handle_newsletter",
            "handle_personal": "handle_personal",
            "handle_spam": "handle_spam"
        }
    )
    
    # All handlers end
    for handler in ["handle_urgent", "handle_meeting", "handle_newsletter", 
                    "handle_personal", "handle_spam"]:
        graph.add_edge(handler, END)
    
    return graph.compile()


# === MAIN ===

def main():
    app = create_email_graph()
    
    test_emails = [
        {"sender": "boss@company.com", "subject": "URGENT: Server down!", 
         "body": "Production crashed. Need help immediately!"},
        {"sender": "calendar@company.com", "subject": "Meeting: Q4 Planning",
         "body": "Friday at 2pm in Conference Room A."},
        {"sender": "deals@store.com", "subject": "50% OFF Today Only!",
         "body": "Our biggest sale of the year!"},
        {"sender": "mom@email.com", "subject": "Sunday dinner?",
         "body": "Are you coming for dinner? Love, Mom"},
        {"sender": "prince@scam.com", "subject": "You won $1,000,000!",
         "body": "Send your bank details to claim..."}
    ]
    
    print("=" * 60)
    print("📬 Email Classifier")
    print("=" * 60)
    
    for email in test_emails:
        print(f"\n📩 From: {email['sender']}")
        print(f"   Subject: {email['subject']}")
        print("-" * 40)
        
        result = app.invoke({
            "email_subject": email["subject"],
            "email_body": email["body"],
            "sender": email["sender"],
            "category": "",
            "action_taken": "",
            "extracted_info": {}
        })
        
        print(f"   Action: {result['action_taken']}")


if __name__ == "__main__":
    main()
