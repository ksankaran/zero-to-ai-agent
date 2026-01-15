# From: Zero to AI Agent, Chapter 16, Section 16.2
# File: supervisor_pattern.py

"""
Supervisor pattern: Routes requests to appropriate specialists.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


class CustomerState(TypedDict):
    request: str
    category: str
    response: str


def supervisor(state: CustomerState) -> dict:
    """Analyzes request and determines routing."""
    prompt = f"""Categorize this customer request into exactly one category:
    - billing (payment, charges, invoices, refunds)
    - technical (bugs, errors, how-to, features)
    - general (other questions, feedback, complaints)
    
    Request: {state['request']}
    
    Reply with just the category name."""
    
    response = llm.invoke(prompt)
    category = response.content.strip().lower()
    
    # Normalize to valid categories
    if "billing" in category:
        category = "billing"
    elif "technical" in category:
        category = "technical"
    else:
        category = "general"
    
    print(f"🎯 Supervisor routed to: {category}")
    return {"category": category}


def billing_agent(state: CustomerState) -> dict:
    """Handles billing-related requests."""
    prompt = f"""You are a billing specialist. Help with this request:
    {state['request']}
    
    Be helpful and mention relevant policies."""
    
    response = llm.invoke(prompt)
    print("💳 Billing agent responded")
    return {"response": response.content}


def technical_agent(state: CustomerState) -> dict:
    """Handles technical support requests."""
    prompt = f"""You are a technical support specialist. Help with:
    {state['request']}
    
    Provide clear steps and explanations."""
    
    response = llm.invoke(prompt)
    print("🔧 Technical agent responded")
    return {"response": response.content}


def general_agent(state: CustomerState) -> dict:
    """Handles general inquiries."""
    prompt = f"""You are a customer service representative. Help with:
    {state['request']}
    
    Be friendly and helpful."""
    
    response = llm.invoke(prompt)
    print("💬 General agent responded")
    return {"response": response.content}


def route_to_worker(state: CustomerState) -> Literal["billing", "technical", "general"]:
    """Routes to the appropriate worker based on category."""
    return state["category"]


workflow = StateGraph(CustomerState)

workflow.add_node("supervisor", supervisor)
workflow.add_node("billing", billing_agent)
workflow.add_node("technical", technical_agent)
workflow.add_node("general", general_agent)

# Supervisor first
workflow.add_edge(START, "supervisor")

# Conditional routing based on supervisor's decision
workflow.add_conditional_edges(
    "supervisor",
    route_to_worker,
    {
        "billing": "billing",
        "technical": "technical",
        "general": "general"
    }
)

# All workers go to END
workflow.add_edge("billing", END)
workflow.add_edge("technical", END)
workflow.add_edge("general", END)

app = workflow.compile()

# Test with different types of requests
requests = [
    "I was charged twice for my subscription last month",
    "The app keeps crashing when I try to upload photos",
    "Do you offer student discounts?"
]

for req in requests:
    print(f"\n{'='*50}")
    print(f"REQUEST: {req}")
    print("=" * 50)
    
    result = app.invoke({
        "request": req,
        "category": "",
        "response": ""
    })
    
    print(f"\nRESPONSE:\n{result['response'][:200]}...")
