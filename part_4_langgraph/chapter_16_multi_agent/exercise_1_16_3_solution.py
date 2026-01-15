# From: Zero to AI Agent, Chapter 16, Section 16.3
# File: exercise_1_16_3_solution.py

"""
Exercise 1 Solution: Customer Service Supervisor

Customer service supervisor with specialists and escalation.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


class ServiceState(TypedDict):
    customer_message: str
    issue_type: str
    routing_count: int
    resolved: bool
    response: str
    needs_human: bool


def greeter(state: ServiceState) -> dict:
    """Welcomes customer and classifies their issue."""
    prompt = f"""Analyze this customer message and classify the issue:
    
    Message: {state['customer_message']}
    
    Categories:
    - billing: Payment issues, charges, refunds, subscriptions
    - technical: Bugs, errors, how-to questions, features not working
    - complaint: Unhappy customer, escalation requests, serious issues
    
    Reply with just the category name."""
    
    response = llm.invoke(prompt)
    issue_type = response.content.strip().lower()
    
    if "billing" in issue_type:
        issue_type = "billing"
    elif "technical" in issue_type:
        issue_type = "technical"
    else:
        issue_type = "complaint"
    
    routing_count = state.get("routing_count", 0) + 1
    print(f"👋 Greeter classified as: {issue_type} (routing #{routing_count})")
    
    return {
        "issue_type": issue_type,
        "routing_count": routing_count
    }


def billing_agent(state: ServiceState) -> dict:
    """Handles billing issues."""
    prompt = f"""You are a billing specialist. Help with this issue:
    
    {state['customer_message']}
    
    If you can resolve it, provide the solution.
    If it requires account access you don't have, say "NEEDS_HUMAN".
    
    Keep response under 100 words."""
    
    response = llm.invoke(prompt)
    content = response.content
    
    needs_human = "NEEDS_HUMAN" in content.upper()
    resolved = not needs_human
    
    print(f"💳 Billing agent: {'resolved' if resolved else 'needs escalation'}")
    
    return {
        "response": content.replace("NEEDS_HUMAN", "").strip(),
        "resolved": resolved,
        "needs_human": needs_human
    }


def tech_support(state: ServiceState) -> dict:
    """Handles technical issues."""
    prompt = f"""You are tech support. Help with this issue:
    
    {state['customer_message']}
    
    Provide clear troubleshooting steps.
    If it requires backend access, say "NEEDS_HUMAN".
    
    Keep response under 100 words."""
    
    response = llm.invoke(prompt)
    content = response.content
    
    needs_human = "NEEDS_HUMAN" in content.upper()
    resolved = not needs_human
    
    print(f"🔧 Tech support: {'resolved' if resolved else 'needs escalation'}")
    
    return {
        "response": content.replace("NEEDS_HUMAN", "").strip(),
        "resolved": resolved,
        "needs_human": needs_human
    }


def complaint_handler(state: ServiceState) -> dict:
    """Handles complaints - always escalates serious issues."""
    prompt = f"""You are a complaint specialist. Address this concern:
    
    {state['customer_message']}
    
    Acknowledge the frustration and offer initial help.
    For serious complaints, say "NEEDS_HUMAN" to escalate.
    
    Keep response under 100 words."""
    
    response = llm.invoke(prompt)
    content = response.content
    
    # Complaints often need human touch
    needs_human = "NEEDS_HUMAN" in content.upper() or "serious" in state['customer_message'].lower()
    resolved = not needs_human
    
    print(f"😤 Complaint handler: {'resolved' if resolved else 'needs escalation'}")
    
    return {
        "response": content.replace("NEEDS_HUMAN", "").strip(),
        "resolved": resolved,
        "needs_human": needs_human
    }


def human_handoff(state: ServiceState) -> dict:
    """Prepares case for human agent."""
    handoff_message = f"""
I understand this needs personal attention. I'm connecting you with a human agent.

Summary for the agent:
- Issue Type: {state['issue_type']}
- Customer Message: {state['customer_message'][:200]}...
- Initial Response Attempted: {state['response'][:100]}...

A human agent will be with you shortly. Your estimated wait time is 2-3 minutes.
"""
    print("👤 Escalated to human agent")
    return {"response": handoff_message}


def route_to_specialist(state: ServiceState) -> Literal["billing", "technical", "complaint"]:
    """Routes to appropriate specialist."""
    return state["issue_type"]


def check_resolution(state: ServiceState) -> Literal["done", "human"]:
    """Checks if issue was resolved or needs human."""
    if state.get("needs_human", False):
        return "human"
    return "done"


# Build the workflow
workflow = StateGraph(ServiceState)

workflow.add_node("greeter", greeter)
workflow.add_node("billing", billing_agent)
workflow.add_node("technical", tech_support)
workflow.add_node("complaint", complaint_handler)
workflow.add_node("human_handoff", human_handoff)

workflow.add_edge(START, "greeter")

workflow.add_conditional_edges(
    "greeter",
    route_to_specialist,
    {
        "billing": "billing",
        "technical": "technical",
        "complaint": "complaint"
    }
)

# Check if resolved or needs human
for specialist in ["billing", "technical", "complaint"]:
    workflow.add_conditional_edges(
        specialist,
        check_resolution,
        {
            "done": END,
            "human": "human_handoff"
        }
    )

workflow.add_edge("human_handoff", END)

app = workflow.compile()

# Test with various customer messages
test_messages = [
    "I was charged twice for my subscription this month!",
    "The app crashes every time I try to upload a photo",
    "This is ridiculous! I've been a customer for 5 years and this is how you treat me?",
    "How do I change my password?",
    "I want a refund for the last 3 months of service"
]

print("=" * 60)
print("CUSTOMER SERVICE SYSTEM TEST")
print("=" * 60)

for msg in test_messages:
    print(f"\n{'='*60}")
    print(f"CUSTOMER: {msg}")
    print("-" * 60)
    
    result = app.invoke({
        "customer_message": msg,
        "issue_type": "",
        "routing_count": 0,
        "resolved": False,
        "response": "",
        "needs_human": False
    })
    
    print(f"\nROUTINGS: {result['routing_count']}")
    print(f"RESPONSE:\n{result['response'][:300]}...")
