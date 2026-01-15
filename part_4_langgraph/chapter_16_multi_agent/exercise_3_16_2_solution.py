# From: Zero to AI Agent, Chapter 16, Section 16.2
# File: exercise_3_16_2_solution.py

"""
Exercise 3 Solution: Smart Router with Fallback
Hierarchical pattern: Smart router with specialist agents and fallback.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


class QuestionState(TypedDict):
    question: str
    category: str
    answer: str
    confidence: str


def supervisor(state: QuestionState) -> dict:
    """Routes questions to appropriate specialists."""
    prompt = f"""Categorize this question into exactly ONE category:
    
    - math (calculations, equations, numbers, statistics)
    - history (historical events, dates, people from the past)
    - science (physics, chemistry, biology, nature)
    - fallback (anything else: opinions, current events, how-to, etc.)
    
    Question: {state['question']}
    
    Reply with just the category name."""
    
    response = llm.invoke(prompt)
    category = response.content.strip().lower()
    
    # Normalize category
    if "math" in category:
        category = "math"
    elif "history" in category:
        category = "history"
    elif "science" in category:
        category = "science"
    else:
        category = "fallback"
    
    print(f"🎯 Routed to: {category}")
    return {"category": category}


def math_agent(state: QuestionState) -> dict:
    """Handles math questions."""
    prompt = f"""You are a math expert. Answer this math question:
    
    {state['question']}
    
    Show your work if applicable. Be precise with numbers."""
    
    response = llm.invoke(prompt)
    return {"answer": response.content, "confidence": "high (math specialist)"}


def history_agent(state: QuestionState) -> dict:
    """Handles history questions."""
    prompt = f"""You are a history expert. Answer this history question:
    
    {state['question']}
    
    Include relevant dates and context. Be accurate."""
    
    response = llm.invoke(prompt)
    return {"answer": response.content, "confidence": "high (history specialist)"}


def science_agent(state: QuestionState) -> dict:
    """Handles science questions."""
    prompt = f"""You are a science expert. Answer this science question:
    
    {state['question']}
    
    Explain concepts clearly. Use examples if helpful."""
    
    response = llm.invoke(prompt)
    return {"answer": response.content, "confidence": "high (science specialist)"}


def fallback_agent(state: QuestionState) -> dict:
    """Handles questions that don't fit other categories."""
    prompt = f"""Answer this general question helpfully:
    
    {state['question']}
    
    If you're uncertain, say so. Be helpful but honest."""
    
    response = llm.invoke(prompt)
    return {"answer": response.content, "confidence": "moderate (general knowledge)"}


def route_to_specialist(state: QuestionState) -> Literal["math", "history", "science", "fallback"]:
    """Routes to the appropriate specialist."""
    return state["category"]


# Build the router
workflow = StateGraph(QuestionState)

workflow.add_node("supervisor", supervisor)
workflow.add_node("math", math_agent)
workflow.add_node("history", history_agent)
workflow.add_node("science", science_agent)
workflow.add_node("fallback", fallback_agent)

workflow.add_edge(START, "supervisor")

workflow.add_conditional_edges(
    "supervisor",
    route_to_specialist,
    {
        "math": "math",
        "history": "history",
        "science": "science",
        "fallback": "fallback"
    }
)

workflow.add_edge("math", END)
workflow.add_edge("history", END)
workflow.add_edge("science", END)
workflow.add_edge("fallback", END)

app = workflow.compile()

# Test with various questions
test_questions = [
    "What is 15% of 240?",
    "When did World War II end?",
    "Why is the sky blue?",
    "What's the best programming language to learn?",
    "How many moons does Jupiter have?"
]

print("=" * 60)
print("SMART ROUTER TEST")
print("=" * 60)

for q in test_questions:
    print(f"\n❓ QUESTION: {q}")
    print("-" * 40)
    
    result = app.invoke({
        "question": q,
        "category": "",
        "answer": "",
        "confidence": ""
    })
    
    print(f"📝 ANSWER: {result['answer'][:200]}...")
    print(f"📊 CONFIDENCE: {result['confidence']}")
