# From: Zero to AI Agent, Chapter 16, Section 16.3
# File: iterative_supervisor.py

"""
Supervisor that can call workers multiple times.
"""

from typing import TypedDict, Literal, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import operator

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


class ResearchState(TypedDict):
    query: str
    findings: Annotated[list[str], operator.add]  # Accumulates findings
    iteration: int
    max_iterations: int
    needs_more: bool
    final_report: str


def web_researcher(state: ResearchState) -> dict:
    """Simulates web research (in reality, would use search tools)."""
    prompt = f"""For the query: {state['query']}
    
    Previous findings: {state['findings']}
    
    Provide ONE new finding that hasn't been mentioned yet.
    Be specific and factual. Just the finding, no preamble."""
    
    response = llm.invoke(prompt)
    print(f"🔍 Web researcher found: {response.content[:50]}...")
    return {"findings": [f"[Web] {response.content}"]}


def academic_researcher(state: ResearchState) -> dict:
    """Simulates academic research."""
    prompt = f"""For the query: {state['query']}
    
    Previous findings: {state['findings']}
    
    Provide ONE academic or research-based finding not yet mentioned.
    Cite a plausible source. Just the finding, no preamble."""
    
    response = llm.invoke(prompt)
    print(f"📚 Academic researcher found: {response.content[:50]}...")
    return {"findings": [f"[Academic] {response.content}"]}


def research_supervisor(state: ResearchState) -> dict:
    """Decides whether to continue research or compile results."""
    current_iteration = state.get("iteration", 0) + 1
    max_iter = state.get("max_iterations", 3)
    
    # Check if we have enough findings
    if len(state["findings"]) >= 4 or current_iteration > max_iter:
        print(f"📊 Supervisor: Sufficient findings ({len(state['findings'])})")
        return {"iteration": current_iteration, "needs_more": False}
    
    print(f"📊 Supervisor: Need more research (iteration {current_iteration})")
    return {"iteration": current_iteration, "needs_more": True}


def choose_researcher(state: ResearchState) -> Literal["web", "academic"]:
    """Alternates between research sources."""
    # Simple alternation - could be smarter based on query type
    if len(state["findings"]) % 2 == 0:
        return "web"
    return "academic"


def report_compiler(state: ResearchState) -> dict:
    """Compiles all findings into a final report."""
    findings_text = "\n".join(f"- {f}" for f in state["findings"])
    
    prompt = f"""Compile these research findings into a coherent report:
    
    Query: {state['query']}
    
    Findings:
    {findings_text}
    
    Write a 2-3 paragraph summary that synthesizes the findings."""
    
    response = llm.invoke(prompt)
    print("📝 Report compiled")
    return {"final_report": response.content}


def should_continue(state: ResearchState) -> Literal["research", "compile"]:
    """Decides whether to continue researching or compile."""
    if state.get("needs_more", True):
        return "research"
    return "compile"


def route_researcher(state: ResearchState) -> Literal["web", "academic"]:
    """Routes to specific researcher."""
    return choose_researcher(state)


# Build the iterative workflow
workflow = StateGraph(ResearchState)

workflow.add_node("supervisor", research_supervisor)
workflow.add_node("web", web_researcher)
workflow.add_node("academic", academic_researcher)
workflow.add_node("compiler", report_compiler)

workflow.add_edge(START, "supervisor")

# Supervisor decides: more research or compile
workflow.add_conditional_edges(
    "supervisor",
    should_continue,
    {
        "research": "router",  # Go get more findings
        "compile": "compiler"   # Done, compile report
    }
)

# Router node to pick researcher
workflow.add_node("router", lambda s: {})  # Pass-through
workflow.add_conditional_edges(
    "router",
    route_researcher,
    {
        "web": "web",
        "academic": "academic"
    }
)

# Researchers loop back to supervisor
workflow.add_edge("web", "supervisor")
workflow.add_edge("academic", "supervisor")

workflow.add_edge("compiler", END)

app = workflow.compile()

# Test the iterative research
result = app.invoke({
    "query": "What are the health effects of intermittent fasting?",
    "findings": [],
    "iteration": 0,
    "max_iterations": 3,
    "needs_more": True,
    "final_report": ""
})

print("\n" + "=" * 60)
print("FINAL RESEARCH REPORT")
print("=" * 60)
print(f"\nFindings collected: {len(result['findings'])}")
print(f"\nReport:\n{result['final_report']}")
