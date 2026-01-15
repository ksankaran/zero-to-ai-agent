# From: Building AI Agents, Chapter 14, Section 14.6
# File: exercise_2_14_6_solution.py

"""Multi-stage interview bot with role-based branching.

Exercise 2 Solution: Create an interview bot with three stages:
- Stage 1: Basic info (name, background)
- Stage 2: Technical questions (different paths for engineer vs designer)
- Stage 3: Behavioral questions
"""

import os
from typing import TypedDict, Annotated
from operator import add
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


# === STATE ===

class InterviewState(TypedDict):
    candidate_name: str
    role: str                            # "engineer" or "designer"
    current_stage: int                   # 1, 2, or 3
    questions_asked: Annotated[list, add]
    responses: Annotated[list, add]
    stage_complete: bool
    interview_summary: str


# === STAGE 1: BASIC INFO ===

def stage1_basic_info(state: InterviewState) -> dict:
    """Stage 1: Gather basic information about the candidate."""
    name = state.get("candidate_name", "")
    
    if not name:
        question = "Welcome! What's your name?"
        # Simulated response (real app would get user input)
        return {
            "questions_asked": [question],
            "responses": ["Alex"],
            "candidate_name": "Alex",
            "stage_complete": False
        }
    else:
        question = f"Hi {name}! Tell me about your background."
        return {
            "questions_asked": [question],
            "responses": ["5 years experience..."],
            "stage_complete": True
        }


def check_stage1_complete(state: InterviewState) -> str:
    """Decide whether to continue stage 1 or advance."""
    if state["stage_complete"] and state.get("candidate_name"):
        return "advance_to_stage2"
    return "continue_stage1"


# === STAGE 2: ROLE-BASED TECHNICAL QUESTIONS ===

def advance_to_stage2(state: InterviewState) -> dict:
    """Transition to technical questions."""
    print("📈 Advancing to Stage 2: Technical Questions")
    return {"current_stage": 2, "stage_complete": False}


def route_by_role(state: InterviewState) -> str:
    """Route to role-specific technical questions."""
    role = state.get("role", "engineer").lower()
    if "design" in role:
        return "stage2_designer"
    return "stage2_engineer"


def stage2_engineer(state: InterviewState) -> dict:
    """Technical questions for engineering candidates."""
    questions = [
        "Describe a challenging technical problem you solved.",
        "What's your experience with system design?",
        "How do you approach debugging?"
    ]
    
    asked_count = len([q for q in state["questions_asked"] 
                       if "technical" in q.lower() or "system" in q.lower()])
    
    if asked_count < len(questions):
        q = questions[asked_count]
        print(f"🔧 Engineer Q: {q[:40]}...")
        return {
            "questions_asked": [q],
            "responses": [f"[Response to: {q[:20]}...]"],
            "stage_complete": asked_count >= len(questions) - 1
        }
    return {"stage_complete": True}


def stage2_designer(state: InterviewState) -> dict:
    """Technical questions for design candidates."""
    questions = [
        "Walk me through your design process.",
        "How do you incorporate user feedback?",
        "What prototyping tools do you use?"
    ]
    
    asked_count = len([q for q in state["questions_asked"] 
                       if "design" in q.lower() or "user" in q.lower()])
    
    if asked_count < len(questions):
        q = questions[asked_count]
        print(f"🎨 Designer Q: {q[:40]}...")
        return {
            "questions_asked": [q],
            "responses": [f"[Response to: {q[:20]}...]"],
            "stage_complete": asked_count >= len(questions) - 1
        }
    return {"stage_complete": True}


# === STAGE 3: BEHAVIORAL QUESTIONS ===

def advance_to_stage3(state: InterviewState) -> dict:
    """Transition to behavioral questions."""
    print("📈 Advancing to Stage 3: Behavioral Questions")
    return {"current_stage": 3, "stage_complete": False}


def stage3_behavioral(state: InterviewState) -> dict:
    """Behavioral questions for all candidates."""
    questions = [
        "Tell me about a time you worked with a difficult team member.",
        "Describe meeting a tight deadline.",
        "What motivates you?"
    ]
    
    asked_count = len([q for q in state["questions_asked"] 
                       if "tell me" in q.lower() or "describe" in q.lower()])
    
    if asked_count < len(questions):
        q = questions[asked_count]
        print(f"💭 Behavioral Q: {q[:40]}...")
        return {
            "questions_asked": [q],
            "responses": [f"[Response to: {q[:20]}...]"],
            "stage_complete": asked_count >= len(questions) - 1
        }
    return {"stage_complete": True}


# === SUMMARY ===

def generate_summary(state: InterviewState) -> dict:
    """Generate final interview summary."""
    summary = f"""
Interview Summary for {state['candidate_name']}
Role: {state['role']}
Questions Asked: {len(state['questions_asked'])}
Stages Completed: 3/3
"""
    print("📋 Interview complete!")
    return {"interview_summary": summary.strip()}


# === GRAPH BUILDER ===

def create_interview_graph():
    graph = StateGraph(InterviewState)
    
    # Add all nodes
    graph.add_node("stage1", stage1_basic_info)
    graph.add_node("advance_to_stage2", advance_to_stage2)
    graph.add_node("stage2_engineer", stage2_engineer)
    graph.add_node("stage2_designer", stage2_designer)
    graph.add_node("advance_to_stage3", advance_to_stage3)
    graph.add_node("stage3", stage3_behavioral)
    graph.add_node("summary", generate_summary)
    
    graph.set_entry_point("stage1")
    
    # Stage 1 loop or advance
    graph.add_conditional_edges("stage1", check_stage1_complete, {
        "continue_stage1": "stage1",
        "advance_to_stage2": "advance_to_stage2"
    })
    
    # Stage 2 role branching
    graph.add_conditional_edges("advance_to_stage2", route_by_role, {
        "stage2_engineer": "stage2_engineer",
        "stage2_designer": "stage2_designer"
    })
    
    # Stage 2 loops
    def check_stage2(state):
        return "advance_to_stage3" if state["stage_complete"] else "continue"
    
    graph.add_conditional_edges("stage2_engineer", check_stage2, {
        "continue": "stage2_engineer",
        "advance_to_stage3": "advance_to_stage3"
    })
    graph.add_conditional_edges("stage2_designer", check_stage2, {
        "continue": "stage2_designer", 
        "advance_to_stage3": "advance_to_stage3"
    })
    
    # Stage 3
    graph.add_edge("advance_to_stage3", "stage3")
    
    def check_stage3(state):
        return "summary" if state["stage_complete"] else "continue"
    
    graph.add_conditional_edges("stage3", check_stage3, {
        "continue": "stage3",
        "summary": "summary"
    })
    
    graph.add_edge("summary", END)
    
    return graph.compile()


# === MAIN ===

def main():
    app = create_interview_graph()
    
    print("=" * 60)
    print("🎤 Multi-Stage Interview Bot")
    print("=" * 60)
    
    # Test with engineer
    print("\n--- Engineering Candidate ---")
    result = app.invoke({
        "candidate_name": "",
        "role": "engineer",
        "current_stage": 1,
        "questions_asked": [],
        "responses": [],
        "stage_complete": False,
        "interview_summary": ""
    })
    print(result["interview_summary"])
    
    # Test with designer
    print("\n--- Design Candidate ---")
    result = app.invoke({
        "candidate_name": "",
        "role": "designer",
        "current_stage": 1,
        "questions_asked": [],
        "responses": [],
        "stage_complete": False,
        "interview_summary": ""
    })
    print(result["interview_summary"])


if __name__ == "__main__":
    main()
