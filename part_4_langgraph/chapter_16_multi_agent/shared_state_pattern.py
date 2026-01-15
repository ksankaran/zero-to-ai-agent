# From: Zero to AI Agent, Chapter 16, Section 16.2
# File: shared_state_pattern.py

"""
Shared State pattern: Agents collaborate via common knowledge base.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


class AnalysisState(TypedDict):
    problem: str
    observations: list[str]   # Shared list all agents can append to
    hypothesis: str
    conclusion: str


def data_collector(state: AnalysisState) -> dict:
    """Gathers initial observations about the problem."""
    prompt = f"""Analyze this problem and list 2-3 key observations:
    
    Problem: {state['problem']}
    
    Format: One observation per line, starting with a dash."""
    
    response = llm.invoke(prompt)
    
    # Parse observations and add to shared list
    new_obs = [line.strip("- ").strip() 
               for line in response.content.split("\n") 
               if line.strip().startswith("-")]
    
    print(f"📊 Collector added {len(new_obs)} observations")
    return {"observations": state["observations"] + new_obs}


def pattern_finder(state: AnalysisState) -> dict:
    """Looks for patterns in collected observations."""
    current_obs = "\n".join(f"- {o}" for o in state["observations"])
    
    prompt = f"""Given these observations, identify 1-2 patterns or connections:
    
    {current_obs}
    
    Format: One pattern per line, starting with a dash."""
    
    response = llm.invoke(prompt)
    
    new_patterns = [line.strip("- ").strip() 
                   for line in response.content.split("\n") 
                   if line.strip().startswith("-")]
    
    print(f"🔍 Pattern finder added {len(new_patterns)} patterns")
    return {"observations": state["observations"] + new_patterns}


def hypothesis_maker(state: AnalysisState) -> dict:
    """Forms a hypothesis based on all observations."""
    all_obs = "\n".join(f"- {o}" for o in state["observations"])
    
    prompt = f"""Based on all these observations and patterns:
    
    {all_obs}
    
    Form a single hypothesis explaining the situation.
    Keep it to one sentence."""
    
    response = llm.invoke(prompt)
    print("💡 Hypothesis formed")
    return {"hypothesis": response.content}


def conclusion_maker(state: AnalysisState) -> dict:
    """Draws final conclusion from hypothesis and observations."""
    all_obs = "\n".join(f"- {o}" for o in state["observations"])
    
    prompt = f"""Given:
    Observations: {all_obs}
    Hypothesis: {state['hypothesis']}
    
    Write a brief conclusion with one recommended action."""
    
    response = llm.invoke(prompt)
    print("✅ Conclusion reached")
    return {"conclusion": response.content}


workflow = StateGraph(AnalysisState)

workflow.add_node("collector", data_collector)
workflow.add_node("pattern_finder", pattern_finder)
workflow.add_node("hypothesis_maker", hypothesis_maker)
workflow.add_node("conclusion_maker", conclusion_maker)

workflow.add_edge(START, "collector")
workflow.add_edge("collector", "pattern_finder")
workflow.add_edge("pattern_finder", "hypothesis_maker")
workflow.add_edge("hypothesis_maker", "conclusion_maker")
workflow.add_edge("conclusion_maker", END)

app = workflow.compile()

# Test collaborative analysis
result = app.invoke({
    "problem": "Our e-commerce site's conversion rate dropped 30% last month",
    "observations": [],
    "hypothesis": "",
    "conclusion": ""
})

print("\n" + "=" * 50)
print("SHARED OBSERVATIONS:")
for i, obs in enumerate(result["observations"], 1):
    print(f"  {i}. {obs}")

print("\nHYPOTHESIS:")
print(f"  {result['hypothesis']}")

print("\nCONCLUSION:")
print(f"  {result['conclusion']}")
