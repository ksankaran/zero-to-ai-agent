# From: Zero to AI Agent, Chapter 16, Section 16.4
# File: exercise_3_16_4_solution.py

"""
Exercise 3 Solution: Negotiation Simulation

Negotiation simulation between buyer and seller agents.
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import operator
import re

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.6)


class NegotiationState(TypedDict):
    item: str
    buyer_budget: int
    seller_minimum: int
    current_offer: int
    negotiation_history: Annotated[list[str], operator.add]
    buyer_concessions: Annotated[list[str], operator.add]
    seller_concessions: Annotated[list[str], operator.add]
    round: int
    max_rounds: int
    deal_reached: bool
    final_outcome: str


def buyer_agent(state: NegotiationState) -> dict:
    """Negotiates for lowest price and best terms."""
    round_num = state.get("round", 1)
    history = state.get("negotiation_history", [])
    current_offer = state.get("current_offer", 0)
    budget = state["buyer_budget"]
    
    prompt = f"""You are a BUYER negotiating for: {state['item']}
    
    Your budget: ${budget} (don't reveal this)
    Current seller offer: ${current_offer}
    Round: {round_num} of {state['max_rounds']}
    
    Previous negotiation:
    {chr(10).join(history[-4:])}
    
    Make your move:
    1. State whether you ACCEPT, COUNTER, or WALK AWAY
    2. If COUNTER, propose a specific price and justify it
    3. Try to get below your budget while seeming reasonable
    
    Format: ACTION: [action] | PRICE: $[amount] | REASONING: [brief reason]"""
    
    response = llm.invoke(prompt)
    
    # Parse buyer response
    content = response.content
    action_match = re.search(r'ACTION:\s*(\w+)', content, re.IGNORECASE)
    price_match = re.search(r'PRICE:\s*\$?(\d+)', content, re.IGNORECASE)
    
    action = action_match.group(1).upper() if action_match else "COUNTER"
    new_offer = int(price_match.group(1)) if price_match else current_offer - 50
    
    # Track concession if buyer raised their offer
    concession = ""
    if len(history) > 1 and "BUYER" in history[-2]:
        prev_match = re.search(r'\$(\d+)', history[-2])
        if prev_match and new_offer > int(prev_match.group(1)):
            concession = f"R{round_num}: Raised offer from ${prev_match.group(1)} to ${new_offer}"
    
    print(f"🛒 Buyer (R{round_num}): {action} at ${new_offer}")
    
    result = {
        "negotiation_history": [f"BUYER R{round_num}: {content}"],
        "current_offer": new_offer
    }
    if concession:
        result["buyer_concessions"] = [concession]
    
    return result


def seller_agent(state: NegotiationState) -> dict:
    """Negotiates for highest price and favorable terms."""
    round_num = state.get("round", 1)
    history = state.get("negotiation_history", [])
    current_offer = state.get("current_offer", 0)
    minimum = state["seller_minimum"]
    
    prompt = f"""You are a SELLER negotiating for: {state['item']}
    
    Your minimum acceptable price: ${minimum} (don't reveal this)
    Current buyer offer: ${current_offer}
    Round: {round_num} of {state['max_rounds']}
    
    Previous negotiation:
    {chr(10).join(history[-4:])}
    
    Make your move:
    1. State whether you ACCEPT, COUNTER, or WALK AWAY
    2. If COUNTER, propose a specific price and justify it
    3. Try to get above your minimum while closing the deal
    
    Format: ACTION: [action] | PRICE: $[amount] | REASONING: [brief reason]"""
    
    response = llm.invoke(prompt)
    
    # Parse seller response
    content = response.content
    action_match = re.search(r'ACTION:\s*(\w+)', content, re.IGNORECASE)
    price_match = re.search(r'PRICE:\s*\$?(\d+)', content, re.IGNORECASE)
    
    action = action_match.group(1).upper() if action_match else "COUNTER"
    new_offer = int(price_match.group(1)) if price_match else current_offer + 50
    
    # Check for deal
    deal_reached = action == "ACCEPT"
    
    # Track concession if seller lowered their price
    concession = ""
    if len(history) > 0:
        for h in reversed(history):
            if "SELLER" in h:
                prev_match = re.search(r'\$(\d+)', h)
                if prev_match and new_offer < int(prev_match.group(1)):
                    concession = f"R{round_num}: Lowered price from ${prev_match.group(1)} to ${new_offer}"
                break
    
    print(f"💼 Seller (R{round_num}): {action} at ${new_offer}")
    
    result = {
        "negotiation_history": [f"SELLER R{round_num}: {content}"],
        "current_offer": new_offer,
        "deal_reached": deal_reached
    }
    if concession:
        result["seller_concessions"] = [concession]
    
    return result


def round_manager(state: NegotiationState) -> dict:
    """Advances negotiation rounds."""
    return {"round": state.get("round", 0) + 1}


def should_continue(state: NegotiationState) -> str:
    """Checks if negotiation should continue."""
    if state.get("deal_reached", False):
        return "conclude"
    if state.get("round", 0) >= state.get("max_rounds", 3):
        return "conclude"
    return "continue"


def conclude_negotiation(state: NegotiationState) -> dict:
    """Summarizes negotiation outcome."""
    deal = state.get("deal_reached", False)
    final_price = state.get("current_offer", 0)
    buyer_cons = state.get("buyer_concessions", [])
    seller_cons = state.get("seller_concessions", [])
    
    if deal:
        outcome = f"""
DEAL REACHED! 🤝

Final Price: ${final_price}
Item: {state['item']}

Buyer's Budget: ${state['buyer_budget']}
Seller's Minimum: ${state['seller_minimum']}

Buyer Concessions Made:
{chr(10).join(buyer_cons) if buyer_cons else '- None'}

Seller Concessions Made:
{chr(10).join(seller_cons) if seller_cons else '- None'}

Rounds: {state.get('round', 0)} of {state['max_rounds']}

Value Analysis:
- Buyer saved: ${state['buyer_budget'] - final_price} under budget
- Seller gained: ${final_price - state['seller_minimum']} above minimum
"""
    else:
        outcome = f"""
NO DEAL - IMPASSE 🚫

Last Offer: ${final_price}
Item: {state['item']}

Buyer's Budget: ${state['buyer_budget']}
Seller's Minimum: ${state['seller_minimum']}

Gap: ${abs(final_price - state['seller_minimum']) if final_price < state['seller_minimum'] else 0}

Buyer Concessions Made:
{chr(10).join(buyer_cons) if buyer_cons else '- None'}

Seller Concessions Made:
{chr(10).join(seller_cons) if seller_cons else '- None'}

Rounds Used: {state.get('round', 0)} of {state['max_rounds']}
"""
    
    return {"final_outcome": outcome}


# Build the negotiation workflow
workflow = StateGraph(NegotiationState)

workflow.add_node("round_manager", round_manager)
workflow.add_node("buyer", buyer_agent)
workflow.add_node("seller", seller_agent)
workflow.add_node("conclude", conclude_negotiation)

workflow.add_edge(START, "round_manager")

workflow.add_conditional_edges(
    "round_manager",
    should_continue,
    {
        "continue": "buyer",
        "conclude": "conclude"
    }
)

workflow.add_edge("buyer", "seller")

# Check after seller responds
workflow.add_conditional_edges(
    "seller",
    should_continue,
    {
        "continue": "round_manager",
        "conclude": "conclude"
    }
)

workflow.add_edge("conclude", END)

app = workflow.compile()

# Test the negotiation
result = app.invoke({
    "item": "Used 2020 Honda Civic with 45,000 miles",
    "buyer_budget": 18000,
    "seller_minimum": 15000,
    "current_offer": 12000,  # Buyer's starting offer
    "negotiation_history": [],
    "buyer_concessions": [],
    "seller_concessions": [],
    "round": 0,
    "max_rounds": 3,
    "deal_reached": False,
    "final_outcome": ""
})

print("\n" + "=" * 60)
print("NEGOTIATION OUTCOME")
print("=" * 60)
print(result["final_outcome"])
