# From: Zero to AI Agent, Chapter 17, Section 17.5
# Save as: exercise_3_17_5_solution.py
# Exercise 3: LLM-Designed Research Assistant

import json
from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
creative_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

class ResearchState(TypedDict):
    question: str
    plan: list[dict]  # {"step": name, "description": purpose}
    results: Annotated[list[dict], operator.add]
    final_synthesis: str

# Available research operations
def search_operation(state: ResearchState, description: str) -> dict:
    """Simulate search based on description."""
    response = llm.invoke(
        f"You are researching: {state['question']}\n"
        f"Task: {description}\n"
        f"Provide 3-4 relevant findings as bullet points."
    )
    return {"step": "search", "description": description, "output": response.content}

def analyze_operation(state: ResearchState, description: str) -> dict:
    """Analyze gathered information."""
    context = "\n".join([r["output"] for r in state["results"] if r.get("output")])
    response = llm.invoke(
        f"Question: {state['question']}\n"
        f"Context gathered so far:\n{context}\n\n"
        f"Task: {description}\n"
        f"Provide your analysis."
    )
    return {"step": "analyze", "description": description, "output": response.content}

def compare_operation(state: ResearchState, description: str) -> dict:
    """Compare different aspects or viewpoints."""
    context = "\n".join([r["output"] for r in state["results"] if r.get("output")])
    response = llm.invoke(
        f"Question: {state['question']}\n"
        f"Information:\n{context}\n\n"
        f"Task: {description}\n"
        f"Compare and contrast the key aspects."
    )
    return {"step": "compare", "description": description, "output": response.content}

def evaluate_operation(state: ResearchState, description: str) -> dict:
    """Evaluate sources or claims."""
    context = "\n".join([r["output"] for r in state["results"] if r.get("output")])
    response = llm.invoke(
        f"Question: {state['question']}\n"
        f"Information:\n{context}\n\n"
        f"Task: {description}\n"
        f"Evaluate the credibility and strength of the findings."
    )
    return {"step": "evaluate", "description": description, "output": response.content}

def synthesize_operation(state: ResearchState, description: str) -> dict:
    """Final synthesis of all research."""
    context = "\n\n".join([
        f"[{r['step'].upper()}] {r.get('description', '')}\n{r['output']}" 
        for r in state["results"] if r.get("output")
    ])
    response = creative_llm.invoke(
        f"Research Question: {state['question']}\n\n"
        f"All Research Findings:\n{context}\n\n"
        f"Task: {description}\n"
        f"Provide a comprehensive synthesis answering the original question."
    )
    return {"step": "synthesize", "description": description, "output": response.content}

# Operation registry
OPERATIONS = {
    "search": search_operation,
    "analyze": analyze_operation,
    "compare": compare_operation,
    "evaluate": evaluate_operation,
    "synthesize": synthesize_operation
}

def plan_research(question: str) -> list[dict]:
    """Use LLM to plan research steps."""
    
    available_ops = list(OPERATIONS.keys())
    
    response = llm.invoke(
        f"""You are a research planner. Given a research question, design a workflow.

Research Question: {question}

Available operations: {available_ops}
- search: Find relevant information on a specific aspect
- analyze: Analyze gathered information for patterns/insights
- compare: Compare different viewpoints or aspects
- evaluate: Assess credibility and strength of findings
- synthesize: Combine all findings into final answer (always last)

Create a research plan with 2-5 steps. Each step needs a name and description.
The final step MUST be "synthesize".

Return ONLY a JSON array like:
[
    {{"step": "search", "description": "Find current statistics on topic X"}},
    {{"step": "analyze", "description": "Identify trends in the data"}},
    {{"step": "synthesize", "description": "Combine findings into comprehensive answer"}}
]

Return ONLY the JSON array, no other text."""
    )
    
    try:
        plan = json.loads(response.content)
        
        # Validate and clean up plan
        valid_plan = []
        for item in plan:
            if isinstance(item, dict) and "step" in item and "description" in item:
                if item["step"] in OPERATIONS:
                    valid_plan.append(item)
        
        # Ensure synthesize is at the end
        valid_plan = [p for p in valid_plan if p["step"] != "synthesize"]
        valid_plan.append({"step": "synthesize", "description": "Combine all findings into a comprehensive answer"})
        
        # Ensure at least 2 steps (one task + synthesize)
        if len(valid_plan) < 2:
            valid_plan = [
                {"step": "search", "description": "Find key information about the topic"},
                {"step": "synthesize", "description": "Combine findings into answer"}
            ]
        
        return valid_plan[:5]  # Cap at 5 steps
        
    except (json.JSONDecodeError, TypeError):
        # Fallback plan
        return [
            {"step": "search", "description": "Find key information"},
            {"step": "analyze", "description": "Analyze findings"},
            {"step": "synthesize", "description": "Create final answer"}
        ]

def create_step_node(step_name: str, step_description: str):
    """Create a node function for a research step."""
    
    operation = OPERATIONS.get(step_name, search_operation)
    
    def node_fn(state: ResearchState) -> dict:
        result = operation(state, step_description)
        return {"results": [result]}
    
    return node_fn

def build_research_graph(question: str):
    """Build a research graph based on LLM's plan."""
    
    # Get LLM's research plan
    plan = plan_research(question)
    
    print(f"\n🔬 LLM Research Plan ({len(plan)} steps):")
    for i, step in enumerate(plan, 1):
        print(f"   {i}. [{step['step']}] {step['description']}")
    
    # Build graph
    graph = StateGraph(ResearchState)
    
    # Add nodes for each step
    for i, step in enumerate(plan):
        node_name = f"step_{i}"
        graph.add_node(node_name, create_step_node(step["step"], step["description"]))
    
    # Add final compilation
    def compile_final(state: ResearchState) -> dict:
        # Find the synthesis result
        for r in reversed(state["results"]):
            if r.get("step") == "synthesize":
                return {"final_synthesis": r["output"]}
        return {"final_synthesis": "No synthesis found"}
    
    graph.add_node("compile", compile_final)
    
    # Connect in sequence
    step_names = [f"step_{i}" for i in range(len(plan))]
    
    graph.add_edge(START, step_names[0])
    
    for i in range(len(step_names) - 1):
        graph.add_edge(step_names[i], step_names[i + 1])
    
    graph.add_edge(step_names[-1], "compile")
    graph.add_edge("compile", END)
    
    return graph.compile(), plan

def test_research_assistant():
    questions = [
        "What are the pros and cons of remote work for software teams?",
        "How does climate change affect global food production?",
        "Should companies adopt a 4-day work week?"
    ]
    
    for question in questions:
        print("\n" + "=" * 70)
        print(f"📝 Research Question: {question}")
        print("=" * 70)
        
        graph, plan = build_research_graph(question)
        
        result = graph.invoke({
            "question": question,
            "plan": plan,
            "results": [],
            "final_synthesis": ""
        })
        
        print(f"\n📊 Research Complete!")
        print(f"   Steps executed: {len(result['results'])}")
        print(f"\n{'=' * 70}")
        print("📝 FINAL SYNTHESIS:")
        print("=" * 70)
        print(result["final_synthesis"])

if __name__ == "__main__":
    test_research_assistant()
