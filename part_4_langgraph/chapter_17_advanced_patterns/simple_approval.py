# From: Zero to AI Agent, Chapter 17, Section 17.1
# File: simple_approval.py

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Our workflow state
class ContentState(TypedDict):
    topic: str                    # What to write about
    draft: str                    # The generated content
    status: str                   # Current status


# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

def draft_content(state: ContentState) -> dict:
    """Generate initial content draft."""
    print(f"\n📝 Drafting content about: {state['topic']}")
    
    response = llm.invoke(
        f"Write a short, engaging paragraph about: {state['topic']}"
    )
    
    draft = response.content
    print(f"✅ Draft created ({len(draft)} characters)")
    
    return {
        "draft": draft,
        "status": "draft_complete"
    }


def human_review(state: ContentState) -> dict:
    """Pause for human review and get approval decision."""
    
    print("\n⏸️  Pausing for human review...")
    
    # This is where the magic happens!
    # interrupt() pauses execution and returns this value to the caller
    # When resumed, it returns whatever was passed to Command(resume=...)
    human_decision = interrupt({
        "type": "approval_request",
        "draft": state["draft"],
        "message": "Please review this content. Approve or provide feedback."
    })
    
    # This code only runs AFTER the human responds
    print(f"\n📬 Received human decision: {human_decision}")
    
    if human_decision.get("approved"):
        return {"status": "approved"}
    else:
        # Human rejected - we need to revise
        return {
            "status": "needs_revision",
            "draft": ""  # Clear draft so we regenerate
        }


def revise_content(state: ContentState) -> dict:
    """Revise content based on rejection."""
    print(f"\n🔄 Revising content...")
    
    # In a real app, you'd include the feedback in the prompt
    response = llm.invoke(
        f"Write a different, improved paragraph about: {state['topic']}"
    )
    
    return {
        "draft": response.content,
        "status": "draft_complete"
    }

def publish_content(state: ContentState) -> dict:
    """Publish the approved content."""
    print("\n🚀 Publishing content...")
    print(f"Published: {state['draft'][:100]}...")
    
    return {"status": "published"}


def route_after_review(state: ContentState) -> str:
    """Route based on review outcome."""
    if state["status"] == "approved":
        return "publish"
    elif state["status"] == "needs_revision":
        return "revise"
    else:
        return "review"  # Stay in review

def build_approval_workflow():
    """Build the content approval workflow."""
    
    workflow = StateGraph(ContentState)
    
    # Add nodes
    workflow.add_node("draft", draft_content)
    workflow.add_node("review", human_review)
    workflow.add_node("revise", revise_content)
    workflow.add_node("publish", publish_content)
    
    # Define the flow
    workflow.add_edge(START, "draft")
    workflow.add_edge("draft", "review")
    
    # After review, route based on decision
    workflow.add_conditional_edges(
        "review",
        route_after_review,
        {
            "publish": "publish",
            "revise": "revise",
            "review": "review"
        }
    )
    
    # After revision, go back to review
    workflow.add_edge("revise", "review")
    
    # After publish, we're done
    workflow.add_edge("publish", END)
    
    # Compile with checkpointer (required for interrupts!)
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def run_with_approval():
    """Run the workflow with human-in-the-loop approval."""
    
    app = build_approval_workflow()
    
    # Thread ID identifies this specific workflow instance
    config = {"configurable": {"thread_id": "content-1"}}
    
    print("=" * 50)
    print("🎬 Starting content creation workflow")
    print("=" * 50)
    
    # Initial state
    initial_state = {
        "topic": "Why learning to code is like learning to cook",
        "draft": "",
        "status": "starting"
    }
    
    # Run until interrupt
    result = app.invoke(initial_state, config)

    # Check if we hit an interrupt
    while "__interrupt__" in result or hasattr(result, '__interrupt__'):
        # Get the interrupt payload
        interrupt_info = result.get("__interrupt__", [])
        if interrupt_info:
            payload = interrupt_info[0].value  # Get the first interrupt's value
            
            print("\n" + "=" * 50)
            print("📋 CONTENT FOR REVIEW:")
            print("-" * 50)
            print(payload.get("draft", result.get("draft", "No draft available")))
            print("-" * 50)
            print(payload.get("message", "Please review"))
            
            # Get human decision
            print("\nOptions: [a]pprove, [r]eject, [c]ancel")
            decision = input("Your decision: ").strip().lower()
            
            if decision == 'a':
                # Resume with approval
                result = app.invoke(
                    Command(resume={"approved": True}),
                    config
                )
            elif decision == 'r':
                # Resume with rejection
                feedback = input("Feedback (optional): ").strip()
                result = app.invoke(
                    Command(resume={"approved": False, "feedback": feedback}),
                    config
                )
            elif decision == 'c':
                print("\n❌ Workflow cancelled by user")
                return None
            else:
                print("Invalid option, please try again")
                continue
        else:
            break
    
    print("\n" + "=" * 50)
    print(f"✅ Workflow completed with status: {result.get('status', 'unknown')}")
    print("=" * 50)
    
    return result

if __name__ == "__main__":
    run_with_approval()
