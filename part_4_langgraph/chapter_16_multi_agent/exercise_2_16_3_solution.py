# From: Zero to AI Agent, Chapter 16, Section 16.3
# File: exercise_2_16_3_solution.py

"""
Exercise 2 Solution: Document Processing Pipeline

Iterative document processing with validation loops.
"""

from typing import TypedDict, Literal, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import operator

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


class DocState(TypedDict):
    raw_document: str
    extracted_info: dict
    validation_result: str
    is_complete: bool
    extraction_attempts: int
    max_attempts: int
    enriched_info: dict
    final_document: str


def extractor(state: DocState) -> dict:
    """Extracts key information from document."""
    attempts = state.get("extraction_attempts", 0) + 1
    previous = state.get("extracted_info", {})
    
    prompt = f"""Extract key information from this document:
    
    {state['raw_document']}
    
    Previous extraction (if any): {previous}
    
    Extract:
    - title: Document title or subject
    - date: Any dates mentioned
    - parties: People or organizations mentioned
    - key_points: Main points (list 2-3)
    - action_items: Required actions (if any)
    
    Format as key: value pairs, one per line."""
    
    response = llm.invoke(prompt)
    
    # Parse response into dict (simplified)
    extracted = {"raw_extraction": response.content}
    for line in response.content.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            extracted[key.strip().lower()] = value.strip()
    
    print(f"📋 Extractor completed (attempt {attempts})")
    
    return {
        "extracted_info": extracted,
        "extraction_attempts": attempts
    }


def validator(state: DocState) -> dict:
    """Validates extracted information for completeness."""
    extracted = state.get("extracted_info", {})
    
    required_fields = ["title", "key_points"]
    missing = [f for f in required_fields if f not in extracted or not extracted.get(f)]
    
    if missing:
        result = f"INCOMPLETE: Missing {', '.join(missing)}"
        is_complete = False
    else:
        result = "COMPLETE: All required fields present"
        is_complete = True
    
    print(f"✅ Validator: {result}")
    
    return {
        "validation_result": result,
        "is_complete": is_complete
    }


def enricher(state: DocState) -> dict:
    """Adds additional context to extracted info."""
    extracted = state.get("extracted_info", {})
    
    prompt = f"""Enrich this document information with additional context:
    
    Extracted info: {extracted}
    
    Add:
    - category: What type of document is this?
    - priority: High/Medium/Low based on content
    - summary: One sentence summary
    
    Format as key: value pairs."""
    
    response = llm.invoke(prompt)
    
    enriched = dict(extracted)  # Copy existing
    for line in response.content.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            enriched[key.strip().lower()] = value.strip()
    
    print("🔍 Enricher completed")
    
    return {"enriched_info": enriched}


def compiler(state: DocState) -> dict:
    """Compiles final structured document."""
    enriched = state.get("enriched_info", {})
    
    final_doc = "PROCESSED DOCUMENT\n" + "=" * 40 + "\n"
    for key, value in enriched.items():
        if key != "raw_extraction":
            final_doc += f"{key.upper()}: {value}\n"
    
    final_doc += "=" * 40
    final_doc += f"\nProcessing attempts: {state.get('extraction_attempts', 1)}"
    
    print("📄 Final document compiled")
    
    return {"final_document": final_doc}


def check_validation(state: DocState) -> Literal["retry", "enrich"]:
    """Decides whether to retry extraction or proceed."""
    if state.get("is_complete", False):
        return "enrich"
    
    attempts = state.get("extraction_attempts", 0)
    max_attempts = state.get("max_attempts", 2)
    
    if attempts >= max_attempts:
        print(f"⚠️ Max attempts reached, proceeding anyway")
        return "enrich"
    
    return "retry"


# Build the pipeline
workflow = StateGraph(DocState)

workflow.add_node("extractor", extractor)
workflow.add_node("validator", validator)
workflow.add_node("enricher", enricher)
workflow.add_node("compiler", compiler)

workflow.add_edge(START, "extractor")
workflow.add_edge("extractor", "validator")

workflow.add_conditional_edges(
    "validator",
    check_validation,
    {
        "retry": "extractor",
        "enrich": "enricher"
    }
)

workflow.add_edge("enricher", "compiler")
workflow.add_edge("compiler", END)

app = workflow.compile()

# Test the pipeline
sample_doc = """
MEETING NOTES - Project Alpha Review
Date: March 15, 2024

Attendees: John Smith (PM), Sarah Lee (Dev Lead), Mike Brown (QA)

Discussion Points:
1. Sprint velocity has improved 20% this quarter
2. Customer feedback on new UI is positive
3. Need to address performance issues before launch

Action Items:
- Sarah to optimize database queries by March 20
- Mike to complete regression testing by March 22
- John to schedule stakeholder demo for March 25
"""

result = app.invoke({
    "raw_document": sample_doc,
    "extracted_info": {},
    "validation_result": "",
    "is_complete": False,
    "extraction_attempts": 0,
    "max_attempts": 2,
    "enriched_info": {},
    "final_document": ""
})

print("\n" + "=" * 60)
print("FINAL PROCESSED DOCUMENT")
print("=" * 60)
print(result["final_document"])
