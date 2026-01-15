# From: Zero to AI Agent, Chapter 17, Section 17.4
# Save as: different_state_subgraph.py

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Parent uses these field names
class ParentState(TypedDict):
    user_query: str
    validated_query: str
    search_results: str
    final_answer: str

# Subgraph uses different field names
class ValidationState(TypedDict):
    input_text: str
    is_valid: bool
    cleaned_text: str
    validation_notes: str

def build_validation_subgraph():
    """Build a validation subgraph with its own state schema."""
    
    def check_validity(state: ValidationState) -> dict:
        """Check if input is valid."""
        text = state["input_text"]
        
        # Simple validation rules
        is_valid = len(text) > 3 and not text.isdigit()
        
        return {
            "is_valid": is_valid,
            "validation_notes": "Valid query" if is_valid else "Query too short or invalid"
        }
    
    def clean_text(state: ValidationState) -> dict:
        """Clean and normalize the text."""
        if not state["is_valid"]:
            return {"cleaned_text": ""}
        
        # Clean the text
        cleaned = state["input_text"].strip().lower()
        return {"cleaned_text": cleaned}
    
    subgraph = StateGraph(ValidationState)
    subgraph.add_node("check", check_validity)
    subgraph.add_node("clean", clean_text)
    
    subgraph.add_edge(START, "check")
    subgraph.add_edge("check", "clean")
    subgraph.add_edge("clean", END)
    
    return subgraph.compile()

# Compile subgraph once
validation_subgraph = build_validation_subgraph()

def call_validation_subgraph(state: ParentState) -> dict:
    """Wrapper that transforms state for the validation subgraph."""
    
    # Transform: Parent state → Subgraph state
    subgraph_input = {
        "input_text": state["user_query"],
        "is_valid": False,
        "cleaned_text": "",
        "validation_notes": ""
    }
    
    # Call the subgraph
    subgraph_output = validation_subgraph.invoke(subgraph_input)
    
    # Transform: Subgraph state → Parent state
    return {
        "validated_query": subgraph_output["cleaned_text"]
    }

def search_and_answer(state: ParentState) -> dict:
    """Search and generate answer."""
    query = state["validated_query"]
    
    if not query:
        return {
            "search_results": "",
            "final_answer": "Sorry, I couldn't understand your query."
        }
    
    # Simulate search
    response = llm.invoke(f"Answer this query briefly: {query}")
    
    return {
        "search_results": f"Found results for: {query}",
        "final_answer": response.content
    }

def build_parent_with_transform():
    """Build parent graph with state transformation."""
    
    parent = StateGraph(ParentState)
    
    # Use the wrapper function as a node
    parent.add_node("validate", call_validation_subgraph)
    parent.add_node("search", search_and_answer)
    
    parent.add_edge(START, "validate")
    parent.add_edge("validate", "search")
    parent.add_edge("search", END)
    
    return parent.compile()

def run_different_state_example():
    graph = build_parent_with_transform()
    
    # Test with valid query
    result = graph.invoke({
        "user_query": "What is machine learning?",
        "validated_query": "",
        "search_results": "",
        "final_answer": ""
    })
    
    print("📊 Subgraph Example: Different State Schemas")
    print("=" * 50)
    print(f"\nOriginal Query: {result['user_query']}")
    print(f"Validated Query: {result['validated_query']}")
    print(f"Answer: {result['final_answer'][:200]}...")

if __name__ == "__main__":
    run_different_state_example()
