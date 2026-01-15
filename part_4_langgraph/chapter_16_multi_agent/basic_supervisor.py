# From: Zero to AI Agent, Chapter 16, Section 16.3
# File: basic_supervisor.py

"""
A supervisor that coordinates writing specialists.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


class WritingState(TypedDict):
    request: str
    task_type: str
    draft: str
    final_output: str


def email_writer(state: WritingState) -> dict:
    """Specialist for professional emails."""
    prompt = f"""Write a professional email for this request:
    {state['request']}
    
    Use proper email format with subject line, greeting, body, and signature."""
    
    response = llm.invoke(prompt)
    print("📧 Email writer completed")
    return {"draft": response.content}


def blog_writer(state: WritingState) -> dict:
    """Specialist for blog posts."""
    prompt = f"""Write an engaging blog post for this request:
    {state['request']}
    
    Include a catchy title, introduction, main points, and conclusion."""
    
    response = llm.invoke(prompt)
    print("📝 Blog writer completed")
    return {"draft": response.content}


def summary_writer(state: WritingState) -> dict:
    """Specialist for summaries and briefs."""
    prompt = f"""Write a concise summary for this request:
    {state['request']}
    
    Be brief but comprehensive. Use bullet points if helpful."""
    
    response = llm.invoke(prompt)
    print("📋 Summary writer completed")
    return {"draft": response.content}


def supervisor(state: WritingState) -> dict:
    """Analyzes request and decides which specialist to use."""
    prompt = f"""Analyze this writing request and categorize it:
    
    Request: {state['request']}
    
    Categories:
    - email: Professional correspondence, formal messages, business communication
    - blog: Articles, posts, educational content, opinion pieces
    - summary: Condensing information, briefs, overviews, TL;DR
    
    Reply with just the category name (email, blog, or summary)."""
    
    response = llm.invoke(prompt)
    task_type = response.content.strip().lower()
    
    # Normalize the response
    if "email" in task_type:
        task_type = "email"
    elif "blog" in task_type:
        task_type = "blog"
    else:
        task_type = "summary"
    
    print(f"🎯 Supervisor assigned: {task_type}")
    return {"task_type": task_type}


def finalizer(state: WritingState) -> dict:
    """Reviews and finalizes the draft."""
    prompt = f"""Review this {state['task_type']} draft and make minor improvements:
    
    {state['draft']}
    
    Fix any issues but preserve the style. Return the polished version."""
    
    response = llm.invoke(prompt)
    return {"final_output": response.content}


def route_to_worker(state: WritingState) -> Literal["email", "blog", "summary"]:
    """Routes to the appropriate specialist."""
    return state["task_type"]


# Build the graph
workflow = StateGraph(WritingState)

workflow.add_node("supervisor", supervisor)
workflow.add_node("email", email_writer)
workflow.add_node("blog", blog_writer)
workflow.add_node("summary", summary_writer)
workflow.add_node("finalizer", finalizer)

# Supervisor decides first
workflow.add_edge(START, "supervisor")

# Route to appropriate worker
workflow.add_conditional_edges(
    "supervisor",
    route_to_worker,
    {
        "email": "email",
        "blog": "blog",
        "summary": "summary"
    }
)

# All workers go to finalizer
workflow.add_edge("email", "finalizer")
workflow.add_edge("blog", "finalizer")
workflow.add_edge("summary", "finalizer")

workflow.add_edge("finalizer", END)

app = workflow.compile()

# Test it
requests = [
    "Write to my boss asking for a day off next Friday",
    "Create content about the benefits of remote work",
    "Condense this 10-page report into key takeaways"
]

for req in requests:
    print(f"\n{'='*60}")
    print(f"REQUEST: {req[:50]}...")
    print("=" * 60)
    
    result = app.invoke({
        "request": req,
        "task_type": "",
        "draft": "",
        "final_output": ""
    })
    
    print(f"\nOUTPUT:\n{result['final_output'][:300]}...")
