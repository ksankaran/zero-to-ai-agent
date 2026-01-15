# From: Zero to AI Agent, Chapter 17, Section 17.3
# Save as: exercise_1_17_3_solution.py
# Exercise 1: Multi-Source Fact Checker

import operator
import statistics
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class FactCheckState(TypedDict):
    claim: str
    ratings: Annotated[list[dict], operator.add]
    final_verdict: str

def create_source_checker(source_name: str, source_type: str):
    """Factory to create fact-checking nodes for different sources."""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
    
    def check_claim(state: FactCheckState) -> dict:
        response = llm.invoke(
            f"You are a fact-checker using {source_name} ({source_type}).\n\n"
            f"Claim to verify: {state['claim']}\n\n"
            f"Analyze this claim and provide:\n"
            f"1. Your assessment (2-3 sentences)\n"
            f"2. Accuracy rating from 1-10 (10 = completely true)\n"
            f"3. Key evidence or reasoning\n\n"
            f"End your response with 'RATING: X' where X is your 1-10 score."
        )
        
        content = response.content
        
        # Extract rating from response
        rating = 5  # default
        for line in content.split('\n'):
            if 'RATING:' in line.upper():
                try:
                    rating = int(''.join(filter(str.isdigit, line)))
                    rating = max(1, min(10, rating))  # Clamp to 1-10
                except:
                    pass
        
        print(f"📊 {source_name}: Rating {rating}/10")
        
        return {"ratings": [{
            "source": source_name,
            "source_type": source_type,
            "reasoning": content,
            "rating": rating
        }]}
    
    return check_claim

llm_aggregator = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

def aggregate_ratings(state: FactCheckState) -> dict:
    """Aggregate all ratings and provide final verdict."""
    
    ratings = [r["rating"] for r in state["ratings"]]
    avg_rating = statistics.mean(ratings)
    std_dev = statistics.stdev(ratings) if len(ratings) > 1 else 0
    
    # Determine agreement level
    if std_dev < 1.5:
        agreement = "strong agreement"
    elif std_dev < 2.5:
        agreement = "moderate agreement"
    else:
        agreement = "significant disagreement"
    
    # Compile all reasoning
    all_assessments = "\n\n".join([
        f"{r['source']} ({r['source_type']}): Rating {r['rating']}/10\n{r['reasoning']}"
        for r in state["ratings"]
    ])
    
    # Get final verdict from LLM
    response = llm_aggregator.invoke(
        f"Based on these fact-check assessments:\n\n{all_assessments}\n\n"
        f"Statistics:\n"
        f"- Average rating: {avg_rating:.1f}/10\n"
        f"- Standard deviation: {std_dev:.1f}\n"
        f"- Source agreement: {agreement}\n\n"
        f"Provide a final verdict on the claim with:\n"
        f"1. Overall verdict (TRUE/MOSTLY TRUE/MIXED/MOSTLY FALSE/FALSE)\n"
        f"2. Confidence level based on source agreement\n"
        f"3. Key supporting/contradicting evidence\n"
        f"4. Note any significant disagreements between sources"
    )
    
    verdict = (
        f"📈 Rating: {avg_rating:.1f}/10 (σ={std_dev:.1f})\n"
        f"🤝 Source Agreement: {agreement}\n\n"
        f"{response.content}"
    )
    
    return {"final_verdict": verdict}

def build_fact_checker_graph():
    workflow = StateGraph(FactCheckState)
    
    # Create 4 different source checkers
    workflow.add_node("encyclopedia", create_source_checker(
        "Encyclopedia", "general knowledge database"
    ))
    workflow.add_node("scientific", create_source_checker(
        "Scientific Database", "peer-reviewed research"
    ))
    workflow.add_node("news", create_source_checker(
        "News Archives", "reputable journalism"
    ))
    workflow.add_node("government", create_source_checker(
        "Government Data", "official statistics and records"
    ))
    workflow.add_node("aggregate", aggregate_ratings)
    
    # Fan-out: all sources check in parallel
    workflow.add_edge(START, "encyclopedia")
    workflow.add_edge(START, "scientific")
    workflow.add_edge(START, "news")
    workflow.add_edge(START, "government")
    
    # Fan-in: aggregate all ratings
    workflow.add_edge("encyclopedia", "aggregate")
    workflow.add_edge("scientific", "aggregate")
    workflow.add_edge("news", "aggregate")
    workflow.add_edge("government", "aggregate")
    
    workflow.add_edge("aggregate", END)
    
    return workflow.compile()

def run_fact_checker():
    graph = build_fact_checker_graph()
    
    claims = [
        "The Great Wall of China is visible from space with the naked eye.",
        "Humans use only 10% of their brain capacity.",
        "Water boils at 100°C at sea level under standard atmospheric pressure."
    ]
    
    print("🔍 Multi-Source Fact Checker")
    print("=" * 60)
    
    claim = claims[0]  # Test with first claim
    print(f"\n📝 Claim: {claim}\n")
    print("Checking across 4 sources in parallel...\n")
    
    result = graph.invoke({
        "claim": claim,
        "ratings": [],
        "final_verdict": ""
    })
    
    print("\n" + "=" * 60)
    print("🏆 FINAL VERDICT")
    print("=" * 60)
    print(result["final_verdict"])
    
    # Show individual source ratings
    print("\n📊 Individual Source Ratings:")
    for r in result["ratings"]:
        print(f"  • {r['source']}: {r['rating']}/10")

if __name__ == "__main__":
    run_fact_checker()
