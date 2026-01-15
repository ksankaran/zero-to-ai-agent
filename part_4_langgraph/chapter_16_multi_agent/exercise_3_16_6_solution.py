# From: Zero to AI Agent, Chapter 16, Section 16.6
# File: exercise_3_16_6_solution.py

"""
Exercise 3 Solution: Design a State

Content moderation system with parallel checkers and a decision maker.
Demonstrates proper state design for multi-agent systems.

Agents:
- Toxicity Checker: Scores content for toxic language
- Spam Detector: Checks if content is spam
- PII Scanner: Finds personal information
- Decision Maker: Makes final allow/block decision
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import operator
import re

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)


# =============================================================================
# STATE DESIGN
# =============================================================================

class ModerationState(TypedDict):
    # Input
    content: str
    content_id: str
    
    # Individual checker outputs (each owns their field)
    toxicity_score: float          # 0.0 to 1.0
    toxicity_flags: list[str]      # e.g., ["profanity", "threat"]
    
    spam_score: float              # 0.0 to 1.0
    spam_indicators: list[str]    # e.g., ["repeated_text", "suspicious_links"]
    
    pii_found: list[str]          # e.g., ["email", "phone", "ssn"]
    pii_locations: list[dict]     # e.g., [{"type": "email", "start": 10, "end": 25}]
    
    # Decision maker output
    decision: str                  # "allow", "block", "review"
    decision_reasons: list[str]   # Why this decision was made
    confidence: float              # How confident in the decision
    
    # Tracking
    checks_completed: Annotated[list[str], operator.add]  # Which checks ran


# =============================================================================
# CHECKER AGENTS
# =============================================================================

def toxicity_checker(state: ModerationState) -> dict:
    """Analyzes content for toxic language."""
    content = state["content"]
    
    prompt = f"""Analyze this content for toxicity. Rate from 0.0 (safe) to 1.0 (highly toxic).
    
Content: {content}

Respond in this exact format:
SCORE: [number]
FLAGS: [comma-separated list or "none"]

Example flags: profanity, threat, harassment, hate_speech, none"""

    response = llm.invoke(prompt)
    result = response.content
    
    # Parse response
    score = 0.0
    flags = []
    
    for line in result.split('\n'):
        if line.startswith('SCORE:'):
            try:
                score = float(line.split(':')[1].strip())
                score = max(0.0, min(1.0, score))  # Clamp to 0-1
            except:
                score = 0.5
        elif line.startswith('FLAGS:'):
            flags_str = line.split(':')[1].strip()
            if flags_str.lower() != 'none':
                flags = [f.strip() for f in flags_str.split(',') if f.strip()]
    
    print(f"🔴 Toxicity: score={score:.2f}, flags={flags}")
    
    return {
        "toxicity_score": score,
        "toxicity_flags": flags,
        "checks_completed": ["toxicity"]
    }


def spam_detector(state: ModerationState) -> dict:
    """Checks if content is spam."""
    content = state["content"]
    
    prompt = f"""Analyze this content for spam characteristics. Rate from 0.0 (not spam) to 1.0 (definite spam).
    
Content: {content}

Respond in this exact format:
SCORE: [number]
INDICATORS: [comma-separated list or "none"]

Example indicators: repeated_text, suspicious_links, excessive_caps, sales_pitch, none"""

    response = llm.invoke(prompt)
    result = response.content
    
    # Parse response
    score = 0.0
    indicators = []
    
    for line in result.split('\n'):
        if line.startswith('SCORE:'):
            try:
                score = float(line.split(':')[1].strip())
                score = max(0.0, min(1.0, score))
            except:
                score = 0.5
        elif line.startswith('INDICATORS:'):
            ind_str = line.split(':')[1].strip()
            if ind_str.lower() != 'none':
                indicators = [i.strip() for i in ind_str.split(',') if i.strip()]
    
    print(f"📧 Spam: score={score:.2f}, indicators={indicators}")
    
    return {
        "spam_score": score,
        "spam_indicators": indicators,
        "checks_completed": ["spam"]
    }


def pii_scanner(state: ModerationState) -> dict:
    """Scans for personal identifiable information."""
    content = state["content"]
    
    found = []
    locations = []
    
    # Simple regex-based PII detection
    patterns = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
        "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
    }
    
    for pii_type, pattern in patterns.items():
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        for match in matches:
            if pii_type not in found:
                found.append(pii_type)
            locations.append({
                "type": pii_type,
                "start": match.start(),
                "end": match.end()
            })
    
    print(f"🔒 PII: found={found}")
    
    return {
        "pii_found": found,
        "pii_locations": locations,
        "checks_completed": ["pii"]
    }


# =============================================================================
# DECISION MAKER
# =============================================================================

def decision_maker(state: ModerationState) -> dict:
    """Makes final moderation decision based on all checks."""
    reasons = []
    
    # Evaluate toxicity
    if state["toxicity_score"] > 0.7:
        reasons.append(f"High toxicity ({state['toxicity_score']:.2f}): {state['toxicity_flags']}")
    elif state["toxicity_score"] > 0.4:
        reasons.append(f"Moderate toxicity ({state['toxicity_score']:.2f})")
    
    # Evaluate spam
    if state["spam_score"] > 0.7:
        reasons.append(f"Likely spam ({state['spam_score']:.2f}): {state['spam_indicators']}")
    elif state["spam_score"] > 0.4:
        reasons.append(f"Possible spam ({state['spam_score']:.2f})")
    
    # Evaluate PII
    if state["pii_found"]:
        reasons.append(f"Contains PII: {state['pii_found']}")
    
    # Make decision
    toxicity = state["toxicity_score"]
    spam = state["spam_score"]
    has_pii = len(state["pii_found"]) > 0
    
    if toxicity > 0.8 or (toxicity > 0.6 and "threat" in state["toxicity_flags"]):
        decision = "block"
        confidence = 0.95
    elif spam > 0.8:
        decision = "block"
        confidence = 0.85
    elif has_pii and len(state["pii_found"]) > 1:
        decision = "block"
        confidence = 0.80
    elif toxicity > 0.5 or spam > 0.5 or has_pii:
        decision = "review"
        confidence = 0.70
    else:
        decision = "allow"
        confidence = 0.90
        if not reasons:
            reasons.append("Content passed all checks")
    
    print(f"⚖️ Decision: {decision} (confidence: {confidence:.2f})")
    
    return {
        "decision": decision,
        "decision_reasons": reasons,
        "confidence": confidence
    }


# =============================================================================
# BUILD WORKFLOW
# =============================================================================

workflow = StateGraph(ModerationState)

workflow.add_node("toxicity", toxicity_checker)
workflow.add_node("spam", spam_detector)
workflow.add_node("pii", pii_scanner)
workflow.add_node("decide", decision_maker)

# All checkers run in parallel
workflow.add_edge(START, "toxicity")
workflow.add_edge(START, "spam")
workflow.add_edge(START, "pii")

# All feed into decision maker
workflow.add_edge("toxicity", "decide")
workflow.add_edge("spam", "decide")
workflow.add_edge("pii", "decide")

workflow.add_edge("decide", END)

moderation_system = workflow.compile()


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    # Test cases
    test_cases = [
        {
            "id": "1",
            "content": "Hello! I'd like to share my thoughts on the new product release. Overall, I think it's a great improvement.",
            "description": "Clean content"
        },
        {
            "id": "2", 
            "content": "BUY NOW!!! AMAZING DEAL!!! Click here for FREE MONEY!!! Limited time offer!!!",
            "description": "Obvious spam"
        },
        {
            "id": "3",
            "content": "You can reach me at john.doe@email.com or call 555-123-4567 for more info.",
            "description": "Contains PII"
        }
    ]
    
    print("=" * 60)
    print("CONTENT MODERATION SYSTEM")
    print("=" * 60)
    
    for test in test_cases:
        print(f"\n{'='*60}")
        print(f"Test: {test['description']}")
        print(f"Content: {test['content'][:50]}...")
        print("-" * 40)
        
        result = moderation_system.invoke({
            "content": test["content"],
            "content_id": test["id"],
            "toxicity_score": 0.0,
            "toxicity_flags": [],
            "spam_score": 0.0,
            "spam_indicators": [],
            "pii_found": [],
            "pii_locations": [],
            "decision": "",
            "decision_reasons": [],
            "confidence": 0.0,
            "checks_completed": []
        })
        
        print(f"\nFinal Decision: {result['decision'].upper()}")
        print(f"Confidence: {result['confidence']:.0%}")
        print(f"Reasons: {result['decision_reasons']}")
        print(f"Checks completed: {result['checks_completed']}")
