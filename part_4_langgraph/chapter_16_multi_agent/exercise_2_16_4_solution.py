# From: Zero to AI Agent, Chapter 16, Section 16.4
# File: exercise_2_16_4_solution.py

"""
Exercise 2 Solution: Review Committee

Collaborative review committee with three specialists.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)


class ReviewState(TypedDict):
    content: str
    target_audience: str
    technical_review: str
    style_review: str
    audience_review: str
    consolidated_review: str


def technical_reviewer(state: ReviewState) -> dict:
    """Checks accuracy and technical correctness."""
    prompt = f"""As a TECHNICAL REVIEWER, evaluate this content:
    
    {state['content']}
    
    Focus ONLY on:
    - Factual accuracy
    - Technical correctness
    - Logical consistency
    - Missing important details
    
    List issues as: [CRITICAL], [MAJOR], or [MINOR]
    End with a technical quality score: 1-10"""
    
    response = llm.invoke(prompt)
    print("🔬 Technical review complete")
    return {"technical_review": response.content}


def style_reviewer(state: ReviewState) -> dict:
    """Checks clarity and readability."""
    prompt = f"""As a STYLE REVIEWER, evaluate this content:
    
    {state['content']}
    
    Focus ONLY on:
    - Clarity of expression
    - Sentence structure
    - Word choice
    - Flow and organization
    
    List issues as: [CRITICAL], [MAJOR], or [MINOR]
    End with a style quality score: 1-10"""
    
    response = llm.invoke(prompt)
    print("✍️ Style review complete")
    return {"style_review": response.content}


def audience_reviewer(state: ReviewState) -> dict:
    """Checks appropriateness for target audience."""
    prompt = f"""As an AUDIENCE REVIEWER, evaluate this content:
    
    TARGET AUDIENCE: {state['target_audience']}
    
    CONTENT:
    {state['content']}
    
    Focus ONLY on:
    - Is the complexity appropriate?
    - Will the audience understand the terminology?
    - Does it address audience needs/interests?
    - Is the tone appropriate?
    
    List issues as: [CRITICAL], [MAJOR], or [MINOR]
    End with an audience fit score: 1-10"""
    
    response = llm.invoke(prompt)
    print("👥 Audience review complete")
    return {"audience_review": response.content}


def consolidator(state: ReviewState) -> dict:
    """Creates prioritized consolidated review."""
    prompt = f"""Consolidate these three reviews into a single actionable report:
    
    TECHNICAL REVIEW:
    {state['technical_review']}
    
    STYLE REVIEW:
    {state['style_review']}
    
    AUDIENCE REVIEW:
    {state['audience_review']}
    
    Create a consolidated review with:
    
    1. OVERALL ASSESSMENT (one paragraph)
    
    2. PRIORITY FIXES (must address before publishing):
       - List critical and major issues from all reviews
       - Prioritize by impact
    
    3. SUGGESTED IMPROVEMENTS (nice to have):
       - List minor issues
       - Group by category
    
    4. OVERALL SCORE: Average of the three scores
    
    Be specific and actionable."""
    
    response = llm.invoke(prompt)
    print("📋 Reviews consolidated")
    return {"consolidated_review": response.content}


# Build the workflow
workflow = StateGraph(ReviewState)

workflow.add_node("technical", technical_reviewer)
workflow.add_node("style", style_reviewer)
workflow.add_node("audience", audience_reviewer)
workflow.add_node("consolidator", consolidator)

# All three reviews happen in parallel
workflow.add_edge(START, "technical")
workflow.add_edge(START, "style")
workflow.add_edge(START, "audience")

# All feed into consolidator
workflow.add_edge("technical", "consolidator")
workflow.add_edge("style", "consolidator")
workflow.add_edge("audience", "consolidator")

workflow.add_edge("consolidator", END)

app = workflow.compile()

# Test the review committee
sample_content = """
Machine learning models utilize gradient descent optimization to minimize 
loss functions. The backpropagation algorithm computes partial derivatives 
through the computational graph, enabling efficient parameter updates. 
Regularization techniques like L2 penalty prevent overfitting by constraining 
the hypothesis space. Cross-validation provides robust estimates of 
generalization error.
"""

result = app.invoke({
    "content": sample_content,
    "target_audience": "Business executives with no technical background",
    "technical_review": "",
    "style_review": "",
    "audience_review": "",
    "consolidated_review": ""
})

print("\n" + "=" * 60)
print("CONSOLIDATED REVIEW REPORT")
print("=" * 60)
print(result["consolidated_review"])
