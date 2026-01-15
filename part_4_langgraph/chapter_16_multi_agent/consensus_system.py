# From: Zero to AI Agent, Chapter 16, Section 16.4
# File: consensus_system.py

"""
Consensus building among multiple agents.
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import operator

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)


class ConsensusState(TypedDict):
    question: str
    proposals: Annotated[list[str], operator.add]
    discussion: Annotated[list[str], operator.add]
    round: int
    max_rounds: int
    consensus_reached: bool
    final_decision: str


def agent_alpha(state: ConsensusState) -> dict:
    """First perspective agent."""
    round_num = state.get("round", 1)
    existing_proposals = state.get("proposals", [])
    existing_discussion = state.get("discussion", [])
    
    if round_num == 1:
        # Initial proposal
        prompt = f"""Propose your answer to: {state['question']}
        
        Give a clear, concise recommendation with brief reasoning."""
    else:
        # Respond to discussion
        prompt = f"""Question: {state['question']}
        
        Previous proposals: {existing_proposals}
        Discussion so far: {existing_discussion}
        
        Based on the discussion, do you:
        1. Maintain your position (explain why)
        2. Modify your position (explain what changed)
        3. Accept another proposal (say which one and why)
        
        Be constructive and aim for consensus."""
    
    response = llm.invoke(prompt)
    
    if round_num == 1:
        return {"proposals": [f"[Alpha] {response.content}"]}
    return {"discussion": [f"[Alpha R{round_num}] {response.content}"]}


def agent_beta(state: ConsensusState) -> dict:
    """Second perspective agent."""
    round_num = state.get("round", 1)
    existing_proposals = state.get("proposals", [])
    existing_discussion = state.get("discussion", [])
    
    if round_num == 1:
        prompt = f"""Propose your answer to: {state['question']}
        
        Consider a different angle than others might take.
        Give a clear recommendation with reasoning."""
    else:
        prompt = f"""Question: {state['question']}
        
        Previous proposals: {existing_proposals}
        Discussion so far: {existing_discussion}
        
        Respond constructively. State if you agree, disagree, or want to modify.
        Focus on finding common ground."""
    
    response = llm.invoke(prompt)
    
    if round_num == 1:
        return {"proposals": [f"[Beta] {response.content}"]}
    return {"discussion": [f"[Beta R{round_num}] {response.content}"]}


def facilitator(state: ConsensusState) -> dict:
    """Checks if consensus has been reached."""
    proposals = state.get("proposals", [])
    discussion = state.get("discussion", [])
    round_num = state.get("round", 0) + 1
    
    if round_num == 1:
        # Just starting, no consensus check yet
        print(f"🗣️ Round {round_num}: Gathering initial proposals")
        return {"round": round_num, "consensus_reached": False}
    
    # Analyze discussion for consensus
    all_content = " ".join(proposals + discussion).lower()
    
    # Simple consensus detection (in production, use LLM for this)
    agreement_signals = ["agree", "accept", "consensus", "common ground", "align"]
    agreement_count = sum(1 for signal in agreement_signals if signal in all_content)
    
    consensus = agreement_count >= 2 or round_num > state.get("max_rounds", 3)
    
    if consensus:
        print(f"✅ Consensus detected after {round_num} rounds")
    else:
        print(f"🗣️ Round {round_num}: Continuing discussion")
    
    return {"round": round_num, "consensus_reached": consensus}


def should_continue(state: ConsensusState) -> str:
    """Decides if discussion should continue."""
    if state.get("consensus_reached", False):
        return "synthesize"
    if state.get("round", 0) >= state.get("max_rounds", 3):
        return "synthesize"
    return "discuss"


def synthesizer(state: ConsensusState) -> dict:
    """Synthesizes discussion into final decision."""
    prompt = f"""Synthesize this group discussion into a final decision:
    
    QUESTION: {state['question']}
    
    INITIAL PROPOSALS:
    {chr(10).join(state.get('proposals', []))}
    
    DISCUSSION:
    {chr(10).join(state.get('discussion', []))}
    
    Provide:
    1. The consensus decision (what the group agreed on)
    2. Key points that led to agreement
    3. Any remaining concerns or caveats"""
    
    response = llm.invoke(prompt)
    print("📋 Final decision synthesized")
    
    return {"final_decision": response.content}


# Build the consensus workflow
workflow = StateGraph(ConsensusState)

workflow.add_node("facilitator", facilitator)
workflow.add_node("alpha", agent_alpha)
workflow.add_node("beta", agent_beta)
workflow.add_node("synthesizer", synthesizer)

workflow.add_edge(START, "facilitator")

workflow.add_conditional_edges(
    "facilitator",
    should_continue,
    {
        "discuss": "alpha",
        "synthesize": "synthesizer"
    }
)

# Discussion flow: alpha -> beta -> facilitator
workflow.add_edge("alpha", "beta")
workflow.add_edge("beta", "facilitator")

workflow.add_edge("synthesizer", END)

app = workflow.compile()

# Test consensus building
result = app.invoke({
    "question": "What programming language should a beginner learn first?",
    "proposals": [],
    "discussion": [],
    "round": 0,
    "max_rounds": 3,
    "consensus_reached": False,
    "final_decision": ""
})

print("\n" + "=" * 60)
print("CONSENSUS DECISION")
print("=" * 60)
print(result["final_decision"])
