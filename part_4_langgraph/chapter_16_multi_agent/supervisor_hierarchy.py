# From: Zero to AI Agent, Chapter 16, Section 16.3
# File: supervisor_hierarchy.py

"""
Two-level supervisor hierarchy for content creation.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


class ContentState(TypedDict):
    topic: str
    stage: str  # "research", "writing", "review", "done"
    research_notes: str
    draft: str
    review_feedback: str
    final_content: str


def research_worker(state: ContentState) -> dict:
    """Gathers information on the topic."""
    prompt = f"List 3 key facts about: {state['topic']}"
    response = llm.invoke(prompt)
    print("  📚 Research worker complete")
    return {"research_notes": response.content}


def writing_worker(state: ContentState) -> dict:
    """Writes content based on research."""
    prompt = f"""Write a short piece about {state['topic']}.
    Use these notes: {state['research_notes']}"""
    response = llm.invoke(prompt)
    print("  ✍️ Writing worker complete")
    return {"draft": response.content}


def review_worker(state: ContentState) -> dict:
    """Reviews and provides feedback."""
    prompt = f"""Review this draft and provide 2 improvement suggestions:
    {state['draft']}"""
    response = llm.invoke(prompt)
    print("  🔍 Review worker complete")
    return {"review_feedback": response.content}


def polish_worker(state: ContentState) -> dict:
    """Applies feedback to create final version."""
    prompt = f"""Improve this draft based on feedback:
    
    Draft: {state['draft']}
    Feedback: {state['review_feedback']}"""
    response = llm.invoke(prompt)
    print("  ✨ Polish worker complete")
    return {"final_content": response.content}


def top_supervisor(state: ContentState) -> dict:
    """High-level supervisor that manages the content pipeline."""
    current_stage = state.get("stage", "research")
    
    stage_order = ["research", "writing", "review", "polish", "done"]
    current_index = stage_order.index(current_stage)
    
    if current_index < len(stage_order) - 1:
        next_stage = stage_order[current_index + 1]
    else:
        next_stage = "done"
    
    print(f"🎯 Top supervisor: {current_stage} → {next_stage}")
    return {"stage": next_stage}


def route_by_stage(state: ContentState) -> Literal["research", "writing", "review", "polish", "done"]:
    """Routes to appropriate stage."""
    return state["stage"]


# Build the hierarchy
workflow = StateGraph(ContentState)

workflow.add_node("top_supervisor", top_supervisor)
workflow.add_node("research", research_worker)
workflow.add_node("writing", writing_worker)
workflow.add_node("review", review_worker)
workflow.add_node("polish", polish_worker)

# Start with supervisor
workflow.add_edge(START, "top_supervisor")

# Route based on stage
workflow.add_conditional_edges(
    "top_supervisor",
    route_by_stage,
    {
        "research": "research",
        "writing": "writing",
        "review": "review",
        "polish": "polish",
        "done": END
    }
)

# Each worker returns to supervisor for next decision
workflow.add_edge("research", "top_supervisor")
workflow.add_edge("writing", "top_supervisor")
workflow.add_edge("review", "top_supervisor")
workflow.add_edge("polish", "top_supervisor")

app = workflow.compile()

# Run the pipeline
result = app.invoke({
    "topic": "The future of renewable energy",
    "stage": "research",
    "research_notes": "",
    "draft": "",
    "review_feedback": "",
    "final_content": ""
})

print("\n" + "=" * 60)
print("FINAL CONTENT")
print("=" * 60)
print(result["final_content"])
