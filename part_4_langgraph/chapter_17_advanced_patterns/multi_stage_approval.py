# From: Zero to AI Agent, Chapter 17, Section 17.1
# File: multi_stage_approval.py

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class DocumentState(TypedDict):
    title: str
    content: str
    current_stage: str
    author_approved: bool
    editor_approved: bool
    legal_approved: bool
    revision_notes: str
    revision_count: int

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


def create_stage_review(stage_name: str, approver_title: str):
    """Factory function to create review nodes for different stages."""
    
    def review_node(state: DocumentState) -> dict:
        print(f"\n{'='*50}")
        print(f"📋 {approver_title} Review Stage")
        print('='*50)
        
        # Request approval from this stage's reviewer
        decision = interrupt({
            "stage": stage_name,
            "approver": approver_title,
            "document_title": state["title"],
            "content_preview": state["content"][:500] + "..." if len(state["content"]) > 500 else state["content"],
            "message": f"{approver_title}: Please review this document."
        })
        
        approved = decision.get("approved", False)
        
        if approved:
            print(f"✅ {approver_title} approved")
            return {
                f"{stage_name}_approved": True,
                "current_stage": f"{stage_name}_complete"
            }
        else:
            print(f"❌ {approver_title} requested changes")
            return {
                f"{stage_name}_approved": False,
                "current_stage": "needs_revision",
                "revision_notes": decision.get("notes", "Please revise")
            }
    
    return review_node

# Create the three review stages
author_review = create_stage_review("author", "Author")
editor_review = create_stage_review("editor", "Editor")
legal_review = create_stage_review("legal", "Legal Team")


def generate_document(state: DocumentState) -> dict:
    """Generate initial document content."""
    print(f"\n📄 Generating document: {state['title']}")
    
    response = llm.invoke(
        f"Write a brief professional document titled '{state['title']}'"
    )
    
    return {
        "content": response.content,
        "current_stage": "author_review"
    }

def revise_document(state: DocumentState) -> dict:
    """Revise document based on feedback."""
    print(f"\n🔄 Revising document (revision #{state['revision_count'] + 1})")
    print(f"   Notes: {state['revision_notes']}")
    
    response = llm.invoke(
        f"Revise this document based on the feedback.\n\n"
        f"Current content:\n{state['content']}\n\n"
        f"Feedback: {state['revision_notes']}\n\n"
        f"Revised document:"
    )
    
    return {
        "content": response.content,
        "revision_count": state["revision_count"] + 1,
        "revision_notes": "",
        "current_stage": "author_review",  # Start over from author
        # Reset all approvals since content changed
        "author_approved": False,
        "editor_approved": False,
        "legal_approved": False
    }

def finalize_document(state: DocumentState) -> dict:
    """Document is fully approved."""
    print("\n🎉 Document approved by all reviewers!")
    return {"current_stage": "finalized"}


def route_document(state: DocumentState) -> str:
    """Route based on current stage and approvals."""
    stage = state["current_stage"]
    
    if stage == "needs_revision":
        return "revise"
    elif stage == "author_review" or (stage == "author_complete" and not state["editor_approved"]):
        if state["author_approved"]:
            return "editor"
        return "author"
    elif stage == "editor_complete" or state["editor_approved"]:
        if state["legal_approved"]:
            return "finalize"
        return "legal"
    elif state["author_approved"] and state["editor_approved"] and state["legal_approved"]:
        return "finalize"
    
    return "author"  # Default to start of review chain

def build_multi_stage_workflow():
    workflow = StateGraph(DocumentState)
    
    workflow.add_node("generate", generate_document)
    workflow.add_node("author", author_review)
    workflow.add_node("editor", editor_review)
    workflow.add_node("legal", legal_review)
    workflow.add_node("revise", revise_document)
    workflow.add_node("finalize", finalize_document)
    
    workflow.add_edge(START, "generate")
    workflow.add_edge("generate", "author")
    
    # Author can approve (-> editor) or reject (-> revise)
    workflow.add_conditional_edges(
        "author",
        lambda s: "editor" if s["author_approved"] else "revise",
        {"editor": "editor", "revise": "revise"}
    )
    
    # Editor can approve (-> legal) or reject (-> revise)
    workflow.add_conditional_edges(
        "editor",
        lambda s: "legal" if s["editor_approved"] else "revise",
        {"legal": "legal", "revise": "revise"}
    )
    
    # Legal can approve (-> finalize) or reject (-> revise)
    workflow.add_conditional_edges(
        "legal",
        lambda s: "finalize" if s["legal_approved"] else "revise",
        {"finalize": "finalize", "revise": "revise"}
    )
    
    # After revision, start the review chain over
    workflow.add_edge("revise", "author")
    
    workflow.add_edge("finalize", END)
    
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


if __name__ == "__main__":
    app = build_multi_stage_workflow()
    config = {"configurable": {"thread_id": "doc-001"}}
    
    initial_state = {
        "title": "Q4 Product Launch Announcement",
        "content": "",
        "current_stage": "starting",
        "author_approved": False,
        "editor_approved": False,
        "legal_approved": False,
        "revision_notes": "",
        "revision_count": 0
    }
    
    result = app.invoke(initial_state, config)
    print(f"\nFinal stage: {result.get('current_stage')}")
