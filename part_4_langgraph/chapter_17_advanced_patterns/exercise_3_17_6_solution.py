# From: Zero to AI Agent, Chapter 17, Section 17.6
# Save as: exercise_3_17_6_solution.py
# Exercise 3: Fact-Checked Article Generator

import json
from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
fact_checker = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

class ArticleState(TypedDict):
    topic: str
    article: str
    claims: list[dict]  # [{"claim": ..., "status": ..., "note": ...}]
    all_claims_verified: bool
    iteration: int
    max_iterations: int
    revision_log: Annotated[list[str], operator.add]

def generate_article(state: ArticleState) -> dict:
    """Generate or revise the article."""
    
    if state["iteration"] == 0:
        prompt = f"""Write a short informative article (3-4 paragraphs) about:
{state['topic']}

Include specific facts, statistics, or claims that can be verified.
Write in an engaging, journalistic style."""
    else:
        # Revise based on fact-check results
        questionable_claims = [c for c in state["claims"] if c["status"] != "VERIFIED"]
        
        prompt = f"""Revise this article to address fact-checking concerns.

Topic: {state['topic']}

Current Article:
{state['article']}

Claims that need revision:
{json.dumps(questionable_claims, indent=2)}

Rewrite the article, either:
1. Correcting inaccurate claims
2. Adding qualifiers to uncertain claims
3. Removing unsupported claims

Write the revised article:"""
    
    response = llm.invoke(prompt)
    
    return {
        "article": response.content,
        "iteration": state["iteration"] + 1,
        "revision_log": [f"Revision {state['iteration'] + 1}"]
    }

def extract_claims(state: ArticleState) -> dict:
    """Extract key claims from the article."""
    
    prompt = f"""Extract 3-5 specific factual claims from this article.
Focus on claims that could be fact-checked (statistics, dates, specific facts).

Article:
{state['article']}

Return ONLY a JSON array of claims:
["claim 1", "claim 2", "claim 3"]"""
    
    response = fact_checker.invoke(prompt)
    
    try:
        claims_list = json.loads(response.content)
        claims = [{"claim": c, "status": "PENDING", "note": ""} for c in claims_list[:5]]
    except json.JSONDecodeError:
        # Fallback: split by newlines
        lines = [l.strip() for l in response.content.split("\n") if l.strip()]
        claims = [{"claim": l, "status": "PENDING", "note": ""} for l in lines[:5]]
    
    return {"claims": claims}

def verify_claims(state: ArticleState) -> dict:
    """Verify each extracted claim."""
    
    verified_claims = []
    
    for claim_obj in state["claims"]:
        claim = claim_obj["claim"]
        
        prompt = f"""Evaluate this claim for factual accuracy:
"{claim}"

Is this claim:
- VERIFIED: Appears factually accurate based on general knowledge
- QUESTIONABLE: May be inaccurate, exaggerated, or needs citation
- UNVERIFIABLE: Cannot be verified without specific sources

Return format:
Status: <VERIFIED/QUESTIONABLE/UNVERIFIABLE>
Note: <brief explanation>"""
        
        response = fact_checker.invoke(prompt)
        content = response.content
        
        # Parse status
        status = "QUESTIONABLE"  # Default
        if "VERIFIED" in content.upper():
            status = "VERIFIED"
        elif "UNVERIFIABLE" in content.upper():
            status = "UNVERIFIABLE"
        
        # Extract note
        note = ""
        if "Note:" in content:
            note = content.split("Note:")[1].strip()[:100]
        
        verified_claims.append({
            "claim": claim,
            "status": status,
            "note": note
        })
    
    # Check if all claims pass
    all_verified = all(c["status"] == "VERIFIED" for c in verified_claims)
    
    return {
        "claims": verified_claims,
        "all_claims_verified": all_verified
    }

def check_article_quality(state: ArticleState) -> str:
    """Decide if article needs revision."""
    
    if state["all_claims_verified"]:
        return "done"
    
    if state["iteration"] >= state["max_iterations"]:
        return "done"
    
    # Check if any claims are questionable
    questionable = [c for c in state["claims"] if c["status"] == "QUESTIONABLE"]
    if questionable:
        return "revise"
    
    return "done"

def build_fact_checked_generator():
    graph = StateGraph(ArticleState)
    
    graph.add_node("generate", generate_article)
    graph.add_node("extract", extract_claims)
    graph.add_node("verify", verify_claims)
    
    graph.add_edge(START, "generate")
    graph.add_edge("generate", "extract")
    graph.add_edge("extract", "verify")
    
    graph.add_conditional_edges(
        "verify",
        check_article_quality,
        {
            "revise": "generate",
            "done": END
        }
    )
    
    return graph.compile()

def test_fact_checked_generator():
    graph = build_fact_checked_generator()
    
    topics = [
        "The benefits and risks of artificial intelligence in healthcare",
        "Climate change impacts on global agriculture"
    ]
    
    for topic in topics:
        print("\n" + "=" * 70)
        print(f"📰 Topic: {topic}")
        print("=" * 70)
        
        result = graph.invoke({
            "topic": topic,
            "article": "",
            "claims": [],
            "all_claims_verified": False,
            "iteration": 0,
            "max_iterations": 3,
            "revision_log": []
        })
        
        print(f"\nIterations: {result['iteration']}")
        print(f"All claims verified: {'Yes ✅' if result['all_claims_verified'] else 'No'}")
        
        print("\n📋 Claims Verification:")
        for claim in result["claims"]:
            status_icon = {
                "VERIFIED": "✅",
                "QUESTIONABLE": "⚠️",
                "UNVERIFIABLE": "❓"
            }.get(claim["status"], "•")
            
            print(f"  {status_icon} [{claim['status']}] {claim['claim'][:60]}...")
            if claim["note"]:
                print(f"      Note: {claim['note'][:60]}...")
        
        print("\n📝 Revision Log:")
        for log in result["revision_log"]:
            print(f"  • {log}")
        
        print(f"\n📰 Final Article:\n{result['article']}")

if __name__ == "__main__":
    test_fact_checked_generator()
