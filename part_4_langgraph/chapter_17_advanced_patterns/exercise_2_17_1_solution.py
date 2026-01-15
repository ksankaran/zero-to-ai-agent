# From: Zero to AI Agent, Chapter 17, Section 17.1
# File: exercise_2_17_1_solution.py
# Exercise: Content Moderation Pipeline

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command
from langchain_openai import ChatOpenAI
from datetime import datetime
import operator
from dotenv import load_dotenv
import json

load_dotenv()

class ModerationState(TypedDict):
    content_id: str
    content: str
    content_type: str
    ai_decision: str
    ai_confidence: float
    ai_reason: str
    final_decision: str
    severity: str
    moderation_log: Annotated[list[str], operator.add]


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


def ai_screen_content(state: ModerationState) -> dict:
    """AI screens content for violations."""
    print(f"\n🤖 AI Screening content: {state['content_id']}")
    
    prompt = f"""Analyze this content for policy violations.

Content type: {state['content_type']}
Content: {state['content']}

Respond in JSON format:
{{
    "decision": "approve" or "flag" or "reject",
    "confidence": 0.0-1.0,
    "reason": "brief explanation",
    "suggested_severity": "none" or "warning" or "removal" or "ban"
}}

- "approve": clearly acceptable content (confidence > 0.9)
- "flag": borderline or uncertain (needs human review)
- "reject": clear violation (confidence > 0.95)"""

    response = llm.invoke(prompt)
    
    try:
        result = json.loads(response.content)
        decision = result.get("decision", "flag")
        confidence = float(result.get("confidence", 0.5))
        reason = result.get("reason", "Analysis complete")
        severity = result.get("suggested_severity", "none")
    except:
        decision = "flag"
        confidence = 0.5
        reason = "AI analysis inconclusive"
        severity = "none"
    
    print(f"   Decision: {decision} (confidence: {confidence:.0%})")
    print(f"   Reason: {reason}")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return {
        "ai_decision": decision,
        "ai_confidence": confidence,
        "ai_reason": reason,
        "severity": severity,
        "moderation_log": [f"[{timestamp}] AI: {decision} ({confidence:.0%}) - {reason}"]
    }


def route_after_ai(state: ModerationState) -> str:
    """Route based on AI decision and confidence."""
    decision = state["ai_decision"]
    confidence = state["ai_confidence"]
    
    if decision == "approve" and confidence > 0.9:
        return "approve"
    elif decision == "reject" and confidence > 0.95:
        return "reject"
    else:
        return "human_review"


def human_review(state: ModerationState) -> dict:
    """Human moderator reviews flagged content."""
    
    print("\n👤 Content flagged for human review")
    
    decision = interrupt({
        "type": "moderator_review",
        "content_id": state["content_id"],
        "content": state["content"],
        "content_type": state["content_type"],
        "ai_decision": state["ai_decision"],
        "ai_confidence": state["ai_confidence"],
        "ai_reason": state["ai_reason"],
        "suggested_severity": state["severity"],
        "message": "Please review this flagged content.",
        "options": ["approve", "warning", "remove", "ban", "escalate"]
    })
    
    action = decision.get("action", "approve")
    reason = decision.get("reason", "")
    moderator = decision.get("moderator", "Moderator")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    if action == "escalate":
        return {
            "final_decision": "escalated",
            "moderation_log": [f"[{timestamp}] Moderator ({moderator}) escalated: {reason}"]
        }
    elif action == "approve":
        return {
            "final_decision": "approved",
            "severity": "none",
            "moderation_log": [f"[{timestamp}] Moderator ({moderator}) approved: {reason}"]
        }
    else:
        return {
            "final_decision": action,
            "severity": action,
            "moderation_log": [f"[{timestamp}] Moderator ({moderator}) action '{action}': {reason}"]
        }


def senior_review(state: ModerationState) -> dict:
    """Senior moderator reviews escalated content."""
    
    print("\n👨‍💼 Content escalated to senior moderator")
    
    decision = interrupt({
        "type": "senior_review",
        "content_id": state["content_id"],
        "content": state["content"],
        "ai_analysis": {
            "decision": state["ai_decision"],
            "confidence": state["ai_confidence"],
            "reason": state["ai_reason"]
        },
        "message": "ESCALATED: Please make final decision on this content.",
        "options": ["approve", "warning", "remove", "ban"]
    })
    
    action = decision.get("action", "remove")
    reason = decision.get("reason", "")
    senior = decision.get("moderator", "Senior Moderator")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    return {
        "final_decision": action,
        "severity": "none" if action == "approve" else action,
        "moderation_log": [f"[{timestamp}] Senior ({senior}) final decision '{action}': {reason}"]
    }


def apply_decision(state: ModerationState) -> dict:
    """Apply the final moderation decision."""
    decision = state["final_decision"]
    
    actions = {
        "approved": "✅ Content approved",
        "warning": "⚠️ Content approved with warning issued",
        "remove": "🗑️ Content removed",
        "ban": "🚫 Content removed, user banned"
    }
    
    print(f"\n{actions.get(decision, '📋 Decision applied')}")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return {
        "moderation_log": [f"[{timestamp}] Action applied: {decision}"]
    }


def auto_approve(state: ModerationState) -> dict:
    """Auto-approve content that AI is confident about."""
    print("\n✅ Content auto-approved by AI")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return {
        "final_decision": "approved",
        "severity": "none",
        "moderation_log": [f"[{timestamp}] Auto-approved (AI confidence > 90%)"]
    }


def auto_reject(state: ModerationState) -> dict:
    """Auto-reject content that AI is confident is violating."""
    print("\n❌ Content auto-rejected by AI")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return {
        "final_decision": "remove",
        "severity": "removal",
        "moderation_log": [f"[{timestamp}] Auto-rejected (AI confidence > 95%): {state['ai_reason']}"]
    }


def route_after_human(state: ModerationState) -> str:
    """Route after human review."""
    if state["final_decision"] == "escalated":
        return "senior"
    return "apply"


def build_moderation_workflow():
    """Build the content moderation workflow."""
    workflow = StateGraph(ModerationState)
    
    workflow.add_node("ai_screen", ai_screen_content)
    workflow.add_node("auto_approve", auto_approve)
    workflow.add_node("auto_reject", auto_reject)
    workflow.add_node("human_review", human_review)
    workflow.add_node("senior_review", senior_review)
    workflow.add_node("apply", apply_decision)
    
    workflow.add_edge(START, "ai_screen")
    
    workflow.add_conditional_edges(
        "ai_screen",
        route_after_ai,
        {
            "approve": "auto_approve",
            "reject": "auto_reject",
            "human_review": "human_review"
        }
    )
    
    workflow.add_edge("auto_approve", "apply")
    workflow.add_edge("auto_reject", "apply")
    
    workflow.add_conditional_edges(
        "human_review",
        route_after_human,
        {
            "senior": "senior_review",
            "apply": "apply"
        }
    )
    
    workflow.add_edge("senior_review", "apply")
    workflow.add_edge("apply", END)
    
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def run_moderation():
    """Interactive runner for content moderation."""
    app = build_moderation_workflow()
    config = {"configurable": {"thread_id": "mod-001"}}
    
    print("\n🛡️ Content Moderation System")
    print("=" * 50)
    content = input("Enter content to moderate:\n> ")
    
    initial_state = {
        "content_id": f"POST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "content": content,
        "content_type": "post",
        "ai_decision": "",
        "ai_confidence": 0.0,
        "ai_reason": "",
        "final_decision": "",
        "severity": "none",
        "moderation_log": []
    }
    
    result = app.invoke(initial_state, config)
    
    # Handle interrupts
    while "__interrupt__" in str(result) or (hasattr(result, 'get') and result.get("__interrupt__")):
        interrupt_data = result.get("__interrupt__", [])
        if not interrupt_data:
            break
            
        payload = interrupt_data[0].value
        review_type = payload.get("type", "review")
        
        print("\n" + "=" * 60)
        print(f"📋 {review_type.upper().replace('_', ' ')}")
        print("=" * 60)
        print(f"Content ID: {payload.get('content_id')}")
        print(f"\nContent:\n{payload.get('content')}")
        
        if "ai_decision" in payload:
            print(f"\n🤖 AI Analysis:")
            print(f"   Decision: {payload['ai_decision']}")
            print(f"   Confidence: {payload['ai_confidence']:.0%}")
            print(f"   Reason: {payload['ai_reason']}")
            print(f"   Suggested: {payload.get('suggested_severity', 'N/A')}")
        
        print(f"\n{payload.get('message')}")
        print("-" * 60)
        
        options = payload.get("options", ["approve", "remove"])
        print(f"\nOptions: {', '.join(options)}")
        action = input("Your decision: ").strip().lower()
        
        if action not in options:
            action = options[0]
            print(f"Invalid option, using: {action}")
        
        reason = input("Reason: ").strip()
        moderator = input("Your name: ").strip() or "Moderator"
        
        result = app.invoke(
            Command(resume={
                "action": action,
                "reason": reason,
                "moderator": moderator
            }),
            config
        )
    
    # Final summary
    print("\n" + "=" * 60)
    print("📊 MODERATION SUMMARY")
    print("=" * 60)
    print(f"Content ID: {result.get('content_id')}")
    print(f"Final Decision: {result.get('final_decision', 'unknown').upper()}")
    print(f"Severity: {result.get('severity', 'none')}")
    print("\n📜 Moderation Log:")
    for entry in result.get("moderation_log", []):
        print(f"  {entry}")
    
    return result


if __name__ == "__main__":
    run_moderation()
