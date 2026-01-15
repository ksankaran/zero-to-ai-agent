# From: Zero to AI Agent, Chapter 16, Section 16.4
# File: exercise_1_16_4_solution.py

"""
Exercise 1 Solution: Three-Way Debate

Three-way debate: Optimist vs Pessimist vs Realist.
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import operator

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


class ThreeWayDebateState(TypedDict):
    topic: str
    optimist_args: Annotated[list[str], operator.add]
    pessimist_args: Annotated[list[str], operator.add]
    realist_args: Annotated[list[str], operator.add]
    round: int
    max_rounds: int
    synthesis: str


def optimist(state: ThreeWayDebateState) -> dict:
    """Focuses on opportunities and benefits."""
    round_num = state.get("round", 1)
    
    prompt = f"""You are the OPTIMIST in a debate about: {state['topic']}
    
    Round {round_num}.
    
    Previous arguments:
    - Optimist: {state.get('optimist_args', [])}
    - Pessimist: {state.get('pessimist_args', [])}
    - Realist: {state.get('realist_args', [])}
    
    Argue for the OPPORTUNITIES and BENEFITS.
    You may respond to pessimist's concerns or build on realist's points.
    Be specific and compelling (2-3 sentences)."""
    
    response = llm.invoke(prompt)
    print(f"😊 Optimist (R{round_num}): {response.content[:50]}...")
    
    return {"optimist_args": [f"[R{round_num}] {response.content}"]}


def pessimist(state: ThreeWayDebateState) -> dict:
    """Focuses on risks and problems."""
    round_num = state.get("round", 1)
    
    prompt = f"""You are the PESSIMIST in a debate about: {state['topic']}
    
    Round {round_num}.
    
    Previous arguments:
    - Optimist: {state.get('optimist_args', [])}
    - Pessimist: {state.get('pessimist_args', [])}
    - Realist: {state.get('realist_args', [])}
    
    Argue about the RISKS and POTENTIAL PROBLEMS.
    Challenge optimist's assumptions and point out what realist might be missing.
    Be specific and substantive (2-3 sentences)."""
    
    response = llm.invoke(prompt)
    print(f"😟 Pessimist (R{round_num}): {response.content[:50]}...")
    
    return {"pessimist_args": [f"[R{round_num}] {response.content}"]}


def realist(state: ThreeWayDebateState) -> dict:
    """Tries to find middle ground."""
    round_num = state.get("round", 1)
    
    prompt = f"""You are the REALIST in a debate about: {state['topic']}
    
    Round {round_num}.
    
    Previous arguments:
    - Optimist: {state.get('optimist_args', [])}
    - Pessimist: {state.get('pessimist_args', [])}
    - Realist: {state.get('realist_args', [])}
    
    Find MIDDLE GROUND and practical truth.
    Acknowledge valid points from both sides.
    Propose balanced perspectives (2-3 sentences)."""
    
    response = llm.invoke(prompt)
    print(f"🤔 Realist (R{round_num}): {response.content[:50]}...")
    
    return {"realist_args": [f"[R{round_num}] {response.content}"]}


def round_manager(state: ThreeWayDebateState) -> dict:
    """Advances debate rounds."""
    current = state.get("round", 0)
    return {"round": current + 1}


def should_continue(state: ThreeWayDebateState) -> str:
    """Checks if debate should continue."""
    if state.get("round", 0) >= state.get("max_rounds", 2):
        return "synthesize"
    return "continue"


def judge(state: ThreeWayDebateState) -> dict:
    """Synthesizes all three perspectives."""
    prompt = f"""As judge, synthesize this three-way debate:
    
    TOPIC: {state['topic']}
    
    OPTIMIST ARGUMENTS:
    {chr(10).join(state.get('optimist_args', []))}
    
    PESSIMIST ARGUMENTS:
    {chr(10).join(state.get('pessimist_args', []))}
    
    REALIST ARGUMENTS:
    {chr(10).join(state.get('realist_args', []))}
    
    Provide:
    1. WHERE ALL THREE PERSPECTIVES ALIGN (common ground)
    2. The strongest unique contribution from each perspective
    3. A balanced final assessment
    4. Recommended action considering all viewpoints"""
    
    response = llm.invoke(prompt)
    print("⚖️ Judge synthesized all perspectives")
    
    return {"synthesis": response.content}


# Build the workflow
workflow = StateGraph(ThreeWayDebateState)

workflow.add_node("round_manager", round_manager)
workflow.add_node("optimist", optimist)
workflow.add_node("pessimist", pessimist)
workflow.add_node("realist", realist)
workflow.add_node("judge", judge)

workflow.add_edge(START, "round_manager")

workflow.add_conditional_edges(
    "round_manager",
    should_continue,
    {
        "continue": "optimist",
        "synthesize": "judge"
    }
)

# All three debate in sequence each round
workflow.add_edge("optimist", "pessimist")
workflow.add_edge("pessimist", "realist")
workflow.add_edge("realist", "round_manager")

workflow.add_edge("judge", END)

app = workflow.compile()

# Test the three-way debate
result = app.invoke({
    "topic": "Companies should require employees to return to office full-time",
    "optimist_args": [],
    "pessimist_args": [],
    "realist_args": [],
    "round": 0,
    "max_rounds": 2,
    "synthesis": ""
})

print("\n" + "=" * 60)
print("THREE-WAY DEBATE SYNTHESIS")
print("=" * 60)
print(result["synthesis"])
