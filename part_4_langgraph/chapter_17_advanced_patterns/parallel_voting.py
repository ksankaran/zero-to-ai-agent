# From: Zero to AI Agent, Chapter 17, Section 17.3
# Save as: parallel_voting.py

import operator
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class VotingState(TypedDict):
    question: str
    context: str
    votes: Annotated[list[dict], operator.add]
    final_decision: str

def create_voter(name: str, perspective: str):
    """Factory function to create voter nodes."""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    
    def vote(state: VotingState) -> dict:
        response = llm.invoke(
            f"You are an expert in {perspective}. "
            f"Question: {state['question']}\n"
            f"Context: {state['context']}\n\n"
            f"Give your opinion in 2-3 sentences, then vote YES or NO on the last line."
        )
        
        content = response.content
        vote_value = "YES" if "YES" in content.upper().split('\n')[-1] else "NO"
        
        print(f"🗳️  {name} voted: {vote_value}")
        
        return {"votes": [{
            "voter": name,
            "perspective": perspective,
            "reasoning": content,
            "vote": vote_value
        }]}
    
    return vote

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

def aggregate_votes(state: VotingState) -> dict:
    """Count votes and make final decision."""
    yes_votes = sum(1 for v in state["votes"] if v["vote"] == "YES")
    no_votes = len(state["votes"]) - yes_votes
    
    # Compile reasoning
    all_reasoning = "\n\n".join([
        f"{v['voter']} ({v['perspective']}): {v['reasoning']}"
        for v in state["votes"]
    ])
    
    response = llm.invoke(
        f"Based on these expert opinions:\n\n{all_reasoning}\n\n"
        f"Votes: {yes_votes} YES, {no_votes} NO\n\n"
        f"Provide a final decision with brief justification."
    )
    
    return {"final_decision": response.content}

def build_voting_graph():
    workflow = StateGraph(VotingState)
    
    # Create diverse voter nodes
    workflow.add_node("technical", create_voter("Technical Expert", "technology and engineering"))
    workflow.add_node("business", create_voter("Business Analyst", "business strategy and ROI"))
    workflow.add_node("ethics", create_voter("Ethics Advisor", "ethics and social impact"))
    workflow.add_node("aggregate", aggregate_votes)
    
    # Fan-out to all voters
    workflow.add_edge(START, "technical")
    workflow.add_edge(START, "business")
    workflow.add_edge(START, "ethics")
    
    # Fan-in to aggregation
    workflow.add_edge("technical", "aggregate")
    workflow.add_edge("business", "aggregate")
    workflow.add_edge("ethics", "aggregate")
    
    workflow.add_edge("aggregate", END)
    
    return workflow.compile()

def run_voting():
    graph = build_voting_graph()
    
    result = graph.invoke({
        "question": "Should we implement AI-powered customer service chatbots?",
        "context": "Our company handles 10,000 customer inquiries daily. "
                   "Current wait times average 15 minutes. "
                   "Implementation cost is $500,000 with ongoing costs of $50,000/year.",
        "votes": [],
        "final_decision": ""
    })
    
    print("\n" + "=" * 50)
    print("📊 Voting Results")
    print("=" * 50)
    
    for vote in result["votes"]:
        print(f"\n{vote['voter']}: {vote['vote']}")
    
    print(f"\n🏆 Final Decision:\n{result['final_decision']}")

if __name__ == "__main__":
    run_voting()
