# From: Zero to AI Agent, Chapter 16, Section 16.2
# File: broadcast_pattern.py

"""
Broadcast pattern: Multiple reviewers analyze the same code.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


class ReviewState(TypedDict):
    code: str
    security_review: str
    performance_review: str
    style_review: str
    summary: str


def security_reviewer(state: ReviewState) -> dict:
    """Reviews code for security issues."""
    prompt = f"""As a security expert, review this code for vulnerabilities:
    
    {state['code']}
    
    List any security concerns (or say 'No issues found')."""
    
    response = llm.invoke(prompt)
    print("🔒 Security review complete")
    return {"security_review": response.content}


def performance_reviewer(state: ReviewState) -> dict:
    """Reviews code for performance issues."""
    prompt = f"""As a performance expert, review this code for efficiency:
    
    {state['code']}
    
    List any performance concerns (or say 'No issues found')."""
    
    response = llm.invoke(prompt)
    print("⚡ Performance review complete")
    return {"performance_review": response.content}


def style_reviewer(state: ReviewState) -> dict:
    """Reviews code for style and readability."""
    prompt = f"""As a code quality expert, review this code for style:
    
    {state['code']}
    
    List any style/readability concerns (or say 'No issues found')."""
    
    response = llm.invoke(prompt)
    print("🎨 Style review complete")
    return {"style_review": response.content}


def aggregator(state: ReviewState) -> dict:
    """Combines all reviews into a summary."""
    prompt = f"""Summarize these code reviews into a brief action list:
    
    Security: {state['security_review']}
    Performance: {state['performance_review']}  
    Style: {state['style_review']}
    
    Prioritize the top 3 issues to fix."""
    
    response = llm.invoke(prompt)
    return {"summary": response.content}


workflow = StateGraph(ReviewState)

workflow.add_node("security", security_reviewer)
workflow.add_node("performance", performance_reviewer)
workflow.add_node("style", style_reviewer)
workflow.add_node("aggregator", aggregator)

# Fan-out: all three reviewers start from START
workflow.add_edge(START, "security")
workflow.add_edge(START, "performance")
workflow.add_edge(START, "style")

# Fan-in: all feed into aggregator
workflow.add_edge("security", "aggregator")
workflow.add_edge("performance", "aggregator")
workflow.add_edge("style", "aggregator")

workflow.add_edge("aggregator", END)

app = workflow.compile()

# Test it with some code
sample_code = """
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = db.execute(query)
    users = []
    for row in result:
        users.append(row)
    return users[0] if users else None
"""

result = app.invoke({
    "code": sample_code,
    "security_review": "",
    "performance_review": "",
    "style_review": "",
    "summary": ""
})

print("\n" + "=" * 50)
print("COMBINED REVIEW SUMMARY:")
print("=" * 50)
print(result["summary"])
