# From: Zero to AI Agent, Chapter 17, Section 17.5
# Save as: llm_driven_graph.py

import json
from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

class TaskState(TypedDict):
    user_request: str
    plan: list[str]
    results: Annotated[list[str], operator.add]
    final_answer: str

# Available operations the LLM can choose from
OPERATIONS = {
    "research": lambda topic: f"Researched: Found key facts about {topic}",
    "summarize": lambda text: f"Summary: Condensed the information",
    "compare": lambda items: f"Comparison: Analyzed differences between items",
    "recommend": lambda criteria: f"Recommendation: Based on criteria, suggest option A",
    "validate": lambda claim: f"Validation: Verified the claim is accurate",
    "format": lambda style: f"Formatted: Output structured as {style}"
}

def create_operation_node(operation: str):
    """Create a node for a specific operation."""
    
    def node_fn(state: TaskState) -> dict:
        # In real implementation, this would do actual work
        op_func = OPERATIONS.get(operation, lambda x: f"Executed {operation}")
        result = op_func(state["user_request"])
        return {"results": [f"[{operation}] {result}"]}
    
    return node_fn

def plan_workflow(user_request: str) -> list[str]:
    """Use LLM to decide what steps are needed."""
    
    available_ops = list(OPERATIONS.keys())
    
    response = llm.invoke(
        f"""Given this user request, decide what operations are needed.
        
User request: {user_request}

Available operations: {available_ops}

Return a JSON array of operation names in the order they should execute.
Example: ["research", "summarize", "format"]

Only return the JSON array, nothing else."""
    )
    
    try:
        plan = json.loads(response.content)
        # Validate operations exist
        plan = [op for op in plan if op in OPERATIONS]
        return plan if plan else ["research"]  # Default fallback
    except json.JSONDecodeError:
        return ["research"]  # Fallback

def build_llm_planned_graph(user_request: str):
    """Build a graph based on LLM's workflow plan."""
    
    # Get LLM's plan
    plan = plan_workflow(user_request)
    print(f"🤖 LLM planned these steps: {plan}")
    
    # Build graph dynamically
    graph = StateGraph(TaskState)
    
    # Add nodes for each planned step
    for operation in plan:
        graph.add_node(operation, create_operation_node(operation))
    
    # Add final compilation node
    def compile_results(state: TaskState) -> dict:
        final = "Final Answer:\n" + "\n".join(state["results"])
        return {"final_answer": final}
    
    graph.add_node("compile", compile_results)
    
    # Connect in sequence
    graph.add_edge(START, plan[0])
    
    for i in range(len(plan) - 1):
        graph.add_edge(plan[i], plan[i + 1])
    
    graph.add_edge(plan[-1], "compile")
    graph.add_edge("compile", END)
    
    return graph.compile(), plan

def test_llm_driven():
    requests = [
        "Compare Python and JavaScript for web development",
        "Research the latest AI trends and summarize them",
        "Validate if quantum computing will replace classical computers soon"
    ]
    
    for request in requests:
        print("\n" + "=" * 60)
        print(f"📝 Request: {request}")
        print("=" * 60)
        
        graph, plan = build_llm_planned_graph(request)
        
        result = graph.invoke({
            "user_request": request,
            "plan": plan,
            "results": [],
            "final_answer": ""
        })
        
        print(f"\n{result['final_answer']}")

if __name__ == "__main__":
    test_llm_driven()
