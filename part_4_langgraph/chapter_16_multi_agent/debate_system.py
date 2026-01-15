# From: Zero to AI Agent, Chapter 16, Section 16.4
# File: debate_system.py

"""
Collaborative debate between agents with opposing viewpoints.
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import operator

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


class DebateState(TypedDict):
    topic: str
    pro_arguments: Annotated[list[str], operator.add]
    con_arguments: Annotated[list[str], operator.add]
    current_round: int
    max_rounds: int
    synthesis: str


def pro_debater(state: DebateState) -> dict:
    """Argues in favor of the topic."""
    existing_pro = state.get("pro_arguments", [])
    existing_con = state.get("con_arguments", [])
    round_num = state.get("current_round", 1)
    
    prompt = f"""You are arguing IN FAVOR of: {state['topic']}
    
    Round {round_num} of the debate.
    
    Previous PRO arguments: {existing_pro}
    Previous CON arguments: {existing_con}
    
    Provide ONE new compelling argument for your position.
    If there are CON arguments, you may also rebut them.
    Be concise but persuasive (2-3 sentences)."""
    
    response = llm.invoke(prompt)
    print(f"✅ PRO (Round {round_num}): {response.content[:60]}...")
    
    return {"pro_arguments": [f"[R{round_num}] {response.content}"]}


def con_debater(state: DebateState) -> dict:
    """Argues against the topic."""
    existing_pro = state.get("pro_arguments", [])
    existing_con = state.get("con_arguments", [])
    round_num = state.get("current_round", 1)
    
    prompt = f"""You are arguing AGAINST: {state['topic']}
    
    Round {round_num} of the debate.
    
    Previous PRO arguments: {existing_pro}
    Previous CON arguments: {existing_con}
    
    Provide ONE new compelling argument against the position.
    You may also rebut PRO arguments.
    Be concise but persuasive (2-3 sentences)."""
    
    response = llm.invoke(prompt)
    print(f"❌ CON (Round {round_num}): {response.content[:60]}...")
    
    return {"con_arguments": [f"[R{round_num}] {response.content}"]}


def round_coordinator(state: DebateState) -> dict:
    """Advances to the next round."""
    current = state.get("current_round", 0)
    return {"current_round": current + 1}


def judge(state: DebateState) -> dict:
    """Synthesizes arguments into a balanced conclusion."""
    pro_args = "\n".join(state.get("pro_arguments", []))
    con_args = "\n".join(state.get("con_arguments", []))
    
    prompt = f"""As an impartial judge, synthesize this debate:
    
    TOPIC: {state['topic']}
    
    ARGUMENTS IN FAVOR:
    {pro_args}
    
    ARGUMENTS AGAINST:
    {con_args}
    
    Provide:
    1. The strongest point from each side
    2. A balanced conclusion
    3. What additional information would help decide
    
    Be fair and analytical."""
    
    response = llm.invoke(prompt)
    print("⚖️ Judge has reached a conclusion")
    
    return {"synthesis": response.content}


def should_continue_debate(state: DebateState) -> str:
    """Checks if debate should continue."""
    current = state.get("current_round", 0)
    max_rounds = state.get("max_rounds", 2)
    
    if current >= max_rounds:
        return "judge"
    return "continue"


# Build the debate workflow
workflow = StateGraph(DebateState)

workflow.add_node("coordinator", round_coordinator)
workflow.add_node("pro", pro_debater)
workflow.add_node("con", con_debater)
workflow.add_node("judge", judge)

# Start with coordinator to set round 1
workflow.add_edge(START, "coordinator")

# After coordinator, check if we should continue
workflow.add_conditional_edges(
    "coordinator",
    should_continue_debate,
    {
        "continue": "pro",
        "judge": "judge"
    }
)

# Pro and Con take turns (both run each round)
workflow.add_edge("pro", "con")
workflow.add_edge("con", "coordinator")  # Back to coordinator for next round

workflow.add_edge("judge", END)

app = workflow.compile()

# Run a debate
result = app.invoke({
    "topic": "Remote work should be the default for knowledge workers",
    "pro_arguments": [],
    "con_arguments": [],
    "current_round": 0,
    "max_rounds": 2,
    "synthesis": ""
})

print("\n" + "=" * 60)
print("DEBATE CONCLUSION")
print("=" * 60)
print(result["synthesis"])
