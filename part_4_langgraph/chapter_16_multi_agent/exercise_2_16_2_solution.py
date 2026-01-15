# From: Zero to AI Agent, Chapter 16, Section 16.2
# File: exercise_2_16_2_solution.py

"""
Exercise 2 Solution: Multi-Perspective Analysis
Broadcast pattern: Three perspectives on a business decision.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


class DecisionState(TypedDict):
    decision: str
    optimist_view: str
    pessimist_view: str
    pragmatist_view: str
    recommendation: str


def optimist_agent(state: DecisionState) -> dict:
    """Focuses on benefits and opportunities."""
    prompt = f"""You are an optimistic business advisor. Analyze this decision:
    
    {state['decision']}
    
    Focus ONLY on:
    - Potential benefits and upsides
    - Growth opportunities
    - Best-case scenarios
    
    Be enthusiastic but specific. Keep to 3-4 points."""
    
    response = llm.invoke(prompt)
    print("🌟 Optimist complete")
    return {"optimist_view": response.content}


def pessimist_agent(state: DecisionState) -> dict:
    """Focuses on risks and problems."""
    prompt = f"""You are a cautious risk analyst. Analyze this decision:
    
    {state['decision']}
    
    Focus ONLY on:
    - Potential risks and downsides
    - Things that could go wrong
    - Worst-case scenarios
    
    Be thorough but fair. Keep to 3-4 points."""
    
    response = llm.invoke(prompt)
    print("⚠️ Pessimist complete")
    return {"pessimist_view": response.content}


def pragmatist_agent(state: DecisionState) -> dict:
    """Focuses on practical implementation."""
    prompt = f"""You are a practical operations manager. Analyze this decision:
    
    {state['decision']}
    
    Focus ONLY on:
    - Implementation requirements
    - Resource needs (time, money, people)
    - Practical challenges and solutions
    
    Be realistic and actionable. Keep to 3-4 points."""
    
    response = llm.invoke(prompt)
    print("🔧 Pragmatist complete")
    return {"pragmatist_view": response.content}


def aggregator_agent(state: DecisionState) -> dict:
    """Synthesizes all perspectives into a recommendation."""
    prompt = f"""Synthesize these three perspectives on a business decision:
    
    DECISION: {state['decision']}
    
    OPTIMIST VIEW:
    {state['optimist_view']}
    
    PESSIMIST VIEW:
    {state['pessimist_view']}
    
    PRAGMATIST VIEW:
    {state['pragmatist_view']}
    
    Provide a balanced recommendation that:
    1. Acknowledges the key opportunity
    2. Addresses the top risk
    3. Outlines the critical first step
    
    Keep to one paragraph."""
    
    response = llm.invoke(prompt)
    print("⚖️ Aggregator complete")
    return {"recommendation": response.content}


# Build broadcast pattern
workflow = StateGraph(DecisionState)

workflow.add_node("optimist", optimist_agent)
workflow.add_node("pessimist", pessimist_agent)
workflow.add_node("pragmatist", pragmatist_agent)
workflow.add_node("aggregator", aggregator_agent)

# Fan-out to all three perspectives
workflow.add_edge(START, "optimist")
workflow.add_edge(START, "pessimist")
workflow.add_edge(START, "pragmatist")

# Fan-in to aggregator
workflow.add_edge("optimist", "aggregator")
workflow.add_edge("pessimist", "aggregator")
workflow.add_edge("pragmatist", "aggregator")

workflow.add_edge("aggregator", END)

app = workflow.compile()

# Test decision
decision = """
We're considering expanding our local bakery into a franchise model. 
We've been profitable for 5 years, have a strong brand, and receive 
frequent requests from entrepreneurs wanting to open locations in 
other cities. This would require significant upfront investment in 
systems, training programs, and legal work.
"""

result = app.invoke({
    "decision": decision,
    "optimist_view": "",
    "pessimist_view": "",
    "pragmatist_view": "",
    "recommendation": ""
})

print("\n" + "=" * 60)
print("MULTI-PERSPECTIVE ANALYSIS")
print("=" * 60)
print(f"\n🌟 OPTIMIST:\n{result['optimist_view']}")
print(f"\n⚠️ PESSIMIST:\n{result['pessimist_view']}")
print(f"\n🔧 PRAGMATIST:\n{result['pragmatist_view']}")
print(f"\n⚖️ RECOMMENDATION:\n{result['recommendation']}")
