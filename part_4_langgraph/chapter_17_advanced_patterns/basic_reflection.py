# From: Zero to AI Agent, Chapter 17, Section 17.6
# Save as: basic_reflection.py

from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
critic_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

class ReflectionState(TypedDict):
    topic: str
    current_draft: str
    critique: str
    iteration: int
    max_iterations: int
    history: Annotated[list[str], operator.add]

def generate_draft(state: ReflectionState) -> dict:
    """Generate initial draft or revision."""
    
    if state["iteration"] == 0:
        # First draft
        prompt = f"Write a short paragraph about: {state['topic']}"
    else:
        # Revision based on critique
        prompt = f"""Improve this draft based on the critique.

Draft:
{state['current_draft']}

Critique:
{state['critique']}

Write an improved version:"""
    
    response = llm.invoke(prompt)
    
    return {
        "current_draft": response.content,
        "history": [f"Draft {state['iteration'] + 1}: {response.content[:100]}..."]
    }

def critique_draft(state: ReflectionState) -> dict:
    """Critique the current draft."""
    
    prompt = f"""Critique this draft. Be specific about what could be improved.
Focus on: clarity, engagement, accuracy, and completeness.

Draft:
{state['current_draft']}

Provide 2-3 specific suggestions for improvement:"""
    
    response = critic_llm.invoke(prompt)
    
    return {
        "critique": response.content,
        "iteration": state["iteration"] + 1,
        "history": [f"Critique {state['iteration'] + 1}: {response.content[:100]}..."]
    }

def should_continue(state: ReflectionState) -> str:
    """Decide whether to continue refining or finish."""
    
    # Stop if max iterations reached
    if state["iteration"] >= state["max_iterations"]:
        return "end"
    
    # Check if critique suggests the draft is good
    critique_lower = state["critique"].lower()
    positive_indicators = ["excellent", "well-written", "no major issues", "good as is"]
    
    if any(indicator in critique_lower for indicator in positive_indicators):
        return "end"
    
    return "revise"

def build_reflection_graph():
    graph = StateGraph(ReflectionState)
    
    graph.add_node("generate", generate_draft)
    graph.add_node("critique", critique_draft)
    
    # Start with generation
    graph.add_edge(START, "generate")
    
    # After generation, always critique
    graph.add_edge("generate", "critique")
    
    # After critique, decide whether to continue
    graph.add_conditional_edges(
        "critique",
        should_continue,
        {
            "revise": "generate",  # Loop back to improve
            "end": END
        }
    )
    
    return graph.compile()

def test_reflection():
    graph = build_reflection_graph()
    
    result = graph.invoke({
        "topic": "The importance of sleep for productivity",
        "current_draft": "",
        "critique": "",
        "iteration": 0,
        "max_iterations": 3,
        "history": []
    })
    
    print("🔄 Reflection Loop Results")
    print("=" * 60)
    print(f"Iterations completed: {result['iteration']}")
    print("\n📜 History:")
    for entry in result["history"]:
        print(f"  • {entry}")
    print(f"\n📝 Final Draft:\n{result['current_draft']}")

if __name__ == "__main__":
    test_reflection()
