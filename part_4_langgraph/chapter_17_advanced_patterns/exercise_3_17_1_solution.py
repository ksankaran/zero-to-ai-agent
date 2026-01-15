# From: Zero to AI Agent, Chapter 17, Section 17.1
# File: exercise_3_17_1_solution.py
# Exercise: Interview Scheduling Assistant

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command
from langchain_openai import ChatOpenAI
from datetime import datetime
import operator
from dotenv import load_dotenv

load_dotenv()

class SchedulingState(TypedDict):
    interview_id: str
    candidate_name: str
    candidate_email: str
    interviewer_name: str
    interviewer_email: str
    position: str
    proposed_slots: list[str]
    selected_slot: str
    confirmed_slot: str
    status: str
    reschedule_count: int
    max_reschedules: int
    history: Annotated[list[str], operator.add]


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)


def propose_times(state: SchedulingState) -> dict:
    """AI proposes available time slots."""
    print(f"\n📅 Generating time slots for {state['candidate_name']}")
    print(f"   Position: {state['position']}")
    
    prompt = """Generate 4 professional interview time slots for next week.
Format each as: "Day, Month Date at Time AM/PM (Timezone)"
Example: "Monday, January 22 at 10:00 AM (EST)"
Just list the 4 options, one per line."""
    
    response = llm.invoke(prompt)
    slots = [s.strip() for s in response.content.strip().split('\n') if s.strip()][:4]
    
    print("   Proposed slots:")
    for i, slot in enumerate(slots, 1):
        print(f"   {i}. {slot}")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return {
        "proposed_slots": slots,
        "status": "slots_proposed",
        "history": [f"[{timestamp}] System proposed {len(slots)} time slots"]
    }


def candidate_selection(state: SchedulingState) -> dict:
    """Candidate selects preferred time using interrupt()."""
    
    print(f"\n📧 Awaiting candidate response...")
    
    decision = interrupt({
        "type": "candidate_selection",
        "recipient": state["candidate_name"],
        "email": state["candidate_email"],
        "position": state["position"],
        "interviewer": state["interviewer_name"],
        "available_slots": state["proposed_slots"],
        "message": "Please select your preferred interview time."
    })
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    action = decision.get("action", "select")
    
    if action == "reschedule":
        if state["reschedule_count"] >= state["max_reschedules"]:
            return {
                "status": "max_reschedules_reached",
                "history": [f"[{timestamp}] Candidate requested reschedule (max reached)"]
            }
        return {
            "status": "reschedule_requested",
            "reschedule_count": state["reschedule_count"] + 1,
            "history": [f"[{timestamp}] Candidate requested different times"]
        }
    
    selected = decision.get("selected_slot", state["proposed_slots"][0])
    return {
        "selected_slot": selected,
        "status": "pending_interviewer",
        "history": [f"[{timestamp}] Candidate selected: {selected}"]
    }


def interviewer_confirmation(state: SchedulingState) -> dict:
    """Interviewer confirms or requests reschedule using interrupt()."""
    
    print(f"\n📧 Awaiting interviewer confirmation...")
    
    decision = interrupt({
        "type": "interviewer_confirmation",
        "recipient": state["interviewer_name"],
        "email": state["interviewer_email"],
        "candidate": state["candidate_name"],
        "position": state["position"],
        "selected_time": state["selected_slot"],
        "message": "Please confirm this interview time or request reschedule."
    })
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    action = decision.get("action", "confirm")
    
    if action == "reschedule":
        reason = decision.get("reason", "Scheduling conflict")
        if state["reschedule_count"] >= state["max_reschedules"]:
            return {
                "status": "max_reschedules_reached",
                "history": [f"[{timestamp}] Interviewer requested reschedule (max reached): {reason}"]
            }
        return {
            "status": "reschedule_requested",
            "reschedule_count": state["reschedule_count"] + 1,
            "history": [f"[{timestamp}] Interviewer requested reschedule: {reason}"]
        }
    
    return {
        "confirmed_slot": state["selected_slot"],
        "status": "confirmed",
        "history": [f"[{timestamp}] Interviewer confirmed: {state['selected_slot']}"]
    }


def send_confirmation(state: SchedulingState) -> dict:
    """Send confirmation to both parties."""
    print(f"\n✅ Interview Confirmed!")
    print(f"   Time: {state['confirmed_slot']}")
    print(f"   Candidate: {state['candidate_name']}")
    print(f"   Interviewer: {state['interviewer_name']}")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return {
        "status": "finalized",
        "history": [
            f"[{timestamp}] Confirmation sent to {state['candidate_email']}",
            f"[{timestamp}] Confirmation sent to {state['interviewer_email']}"
        ]
    }


def handle_max_reschedules(state: SchedulingState) -> dict:
    """Handle when max reschedules reached."""
    print("\n⚠️ Maximum reschedule attempts reached")
    print("   Please contact HR for manual coordination.")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return {
        "status": "needs_manual_intervention",
        "history": [f"[{timestamp}] Escalated to HR - max reschedules exceeded"]
    }


def route_after_candidate(state: SchedulingState) -> str:
    """Route after candidate selection."""
    if state["status"] == "pending_interviewer":
        return "interviewer"
    elif state["status"] == "reschedule_requested":
        return "propose"
    elif state["status"] == "max_reschedules_reached":
        return "max_reached"
    return "candidate"


def route_after_interviewer(state: SchedulingState) -> str:
    """Route after interviewer confirmation."""
    if state["status"] == "confirmed":
        return "confirm"
    elif state["status"] == "reschedule_requested":
        return "propose"
    elif state["status"] == "max_reschedules_reached":
        return "max_reached"
    return "interviewer"


def build_scheduling_workflow():
    """Build the interview scheduling workflow."""
    workflow = StateGraph(SchedulingState)
    
    workflow.add_node("propose", propose_times)
    workflow.add_node("candidate", candidate_selection)
    workflow.add_node("interviewer", interviewer_confirmation)
    workflow.add_node("confirm", send_confirmation)
    workflow.add_node("max_reached", handle_max_reschedules)
    
    workflow.add_edge(START, "propose")
    workflow.add_edge("propose", "candidate")
    
    workflow.add_conditional_edges(
        "candidate",
        route_after_candidate,
        {
            "interviewer": "interviewer",
            "propose": "propose",
            "max_reached": "max_reached",
            "candidate": "candidate"
        }
    )
    
    workflow.add_conditional_edges(
        "interviewer",
        route_after_interviewer,
        {
            "confirm": "confirm",
            "propose": "propose",
            "max_reached": "max_reached",
            "interviewer": "interviewer"
        }
    )
    
    workflow.add_edge("confirm", END)
    workflow.add_edge("max_reached", END)
    
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def run_scheduling():
    """Interactive runner for interview scheduling."""
    app = build_scheduling_workflow()
    config = {"configurable": {"thread_id": "interview-001"}}
    
    initial_state = {
        "interview_id": f"INT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "candidate_name": "Alice Johnson",
        "candidate_email": "alice@email.com",
        "interviewer_name": "Bob Smith",
        "interviewer_email": "bob@company.com",
        "position": "Senior Software Engineer",
        "proposed_slots": [],
        "selected_slot": "",
        "confirmed_slot": "",
        "status": "starting",
        "reschedule_count": 0,
        "max_reschedules": 2,
        "history": []
    }
    
    print("\n🎯 Interview Scheduling Assistant")
    print("=" * 50)
    
    result = app.invoke(initial_state, config)
    
    # Handle interrupts
    while "__interrupt__" in str(result) or (hasattr(result, 'get') and result.get("__interrupt__")):
        interrupt_data = result.get("__interrupt__", [])
        if not interrupt_data:
            break
            
        payload = interrupt_data[0].value
        interrupt_type = payload.get("type", "selection")
        
        print("\n" + "=" * 50)
        print(f"📧 TO: {payload.get('recipient')} ({payload.get('email')})")
        
        if interrupt_type == "candidate_selection":
            print(f"RE: Interview for {payload.get('position')}")
            print("=" * 50)
            print(f"\nDear {payload.get('recipient')},")
            print(f"\n{payload.get('message')}")
            print(f"\nInterviewer: {payload.get('interviewer')}")
            print("\nAvailable times:")
            slots = payload.get("available_slots", [])
            for i, slot in enumerate(slots, 1):
                print(f"  [{i}] {slot}")
            print(f"  [r] Request different times")
            
            choice = input("\nYour selection: ").strip().lower()
            
            if choice == 'r':
                result = app.invoke(
                    Command(resume={"action": "reschedule"}),
                    config
                )
            else:
                try:
                    idx = int(choice) - 1
                    selected = slots[idx] if 0 <= idx < len(slots) else slots[0]
                except:
                    selected = slots[0]
                
                result = app.invoke(
                    Command(resume={"action": "select", "selected_slot": selected}),
                    config
                )
        
        elif interrupt_type == "interviewer_confirmation":
            print(f"RE: Interview Confirmation - {payload.get('candidate')}")
            print("=" * 50)
            print(f"\nCandidate {payload.get('candidate')} has selected:")
            print(f"  📅 {payload.get('selected_time')}")
            print(f"\nPosition: {payload.get('position')}")
            print(f"\n{payload.get('message')}")
            print("\nOptions:")
            print("  [c] Confirm this time")
            print("  [r] Request reschedule")
            
            choice = input("\nYour decision: ").strip().lower()
            
            if choice == 'r':
                reason = input("Reason: ").strip()
                result = app.invoke(
                    Command(resume={"action": "reschedule", "reason": reason}),
                    config
                )
            else:
                result = app.invoke(
                    Command(resume={"action": "confirm"}),
                    config
                )
    
    # Final summary
    print("\n" + "=" * 50)
    print("📊 SCHEDULING SUMMARY")
    print("=" * 50)
    print(f"Interview ID: {result.get('interview_id')}")
    print(f"Status: {result.get('status', 'unknown').upper()}")
    if result.get('confirmed_slot'):
        print(f"Confirmed Time: {result['confirmed_slot']}")
    print(f"Reschedule Attempts: {result.get('reschedule_count', 0)}")
    print("\n📜 History:")
    for entry in result.get("history", []):
        print(f"  {entry}")
    
    return result


if __name__ == "__main__":
    run_scheduling()
