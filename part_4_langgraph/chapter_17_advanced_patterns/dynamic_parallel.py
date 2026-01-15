# From: Zero to AI Agent, Chapter 17, Section 17.3
# Save as: dynamic_parallel.py

import operator
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Main graph state
class MainState(TypedDict):
    topic: str
    questions: list[str]
    # Results from parallel research will be collected here
    answers: Annotated[list[str], operator.add]
    final_report: str

# State for each parallel research task
class QuestionState(TypedDict):
    question: str

def generate_questions(state: MainState) -> dict:
    """Generate research questions about the topic."""
    response = llm.invoke(
        f"Generate exactly 3 specific research questions about: {state['topic']}. "
        "Return only the questions, one per line."
    )
    
    questions = [q.strip() for q in response.content.strip().split('\n') if q.strip()]
    print(f"📋 Generated {len(questions)} questions")
    
    return {"questions": questions}

def route_to_research(state: MainState) -> list[Send]:
    """Create a parallel research task for each question."""
    
    # Return a list of Send objects
    # Each Send creates a parallel branch to the "research" node
    return [
        Send("research", {"question": q}) 
        for q in state["questions"]
    ]

def research_question(state: QuestionState) -> dict:
    """Research a single question."""
    response = llm.invoke(
        f"Briefly answer this question in 2-3 sentences: {state['question']}"
    )
    
    answer = f"Q: {state['question']}\nA: {response.content}"
    print(f"✅ Researched: {state['question'][:50]}...")
    
    # This returns to the MAIN state's "answers" field
    return {"answers": [answer]}

def compile_report(state: MainState) -> dict:
    """Compile all answers into a final report."""
    all_answers = "\n\n".join(state["answers"])
    
    response = llm.invoke(
        f"Create a brief research report about '{state['topic']}' "
        f"based on these Q&As:\n\n{all_answers}"
    )
    
    return {"final_report": response.content}

def build_dynamic_parallel_graph():
    workflow = StateGraph(MainState)
    
    workflow.add_node("generate", generate_questions)
    workflow.add_node("research", research_question)
    workflow.add_node("compile", compile_report)
    
    # Start by generating questions
    workflow.add_edge(START, "generate")
    
    # Use conditional edge with Send for dynamic fan-out
    workflow.add_conditional_edges(
        "generate",
        route_to_research,
        ["research"]  # Possible destinations
    )
    
    # All research tasks feed into compile
    workflow.add_edge("research", "compile")
    workflow.add_edge("compile", END)
    
    return workflow.compile()

def run_dynamic_research():
    graph = build_dynamic_parallel_graph()
    
    result = graph.invoke({
        "topic": "artificial intelligence ethics",
        "questions": [],
        "answers": [],
        "final_report": ""
    })
    
    print("\n" + "=" * 50)
    print("📊 Dynamic Parallel Research Complete!")
    print(f"\nQuestions researched: {len(result['questions'])}")
    print(f"\n📝 Final Report:\n{result['final_report']}")

if __name__ == "__main__":
    run_dynamic_research()
