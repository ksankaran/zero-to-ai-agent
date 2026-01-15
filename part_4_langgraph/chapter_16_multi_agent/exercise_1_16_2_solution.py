# From: Zero to AI Agent, Chapter 16, Section 16.2
# File: exercise_1_16_2_solution.py

"""
Exercise 1 Solution: Document Processing Pipeline
Sequential pipeline: Extract → Classify → Summarize
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


class DocumentState(TypedDict):
    document: str
    entities: str
    doc_type: str
    summary: str


def extractor_agent(state: DocumentState) -> dict:
    """Stage 1: Extract key entities from the document."""
    prompt = f"""Extract key entities from this document:
    
    {state['document']}
    
    List:
    - People mentioned
    - Places mentioned  
    - Dates mentioned
    - Organizations mentioned
    
    Format as bullet points under each category."""
    
    response = llm.invoke(prompt)
    print("📋 Extractor complete")
    return {"entities": response.content}


def classifier_agent(state: DocumentState) -> dict:
    """Stage 2: Classify the document type."""
    prompt = f"""Based on this document and its entities, classify the document type.
    
    Document: {state['document'][:500]}...
    
    Entities found: {state['entities']}
    
    Choose exactly ONE type:
    - legal (contracts, agreements, court documents)
    - medical (health records, prescriptions, clinical notes)
    - financial (invoices, reports, statements)
    - correspondence (letters, emails, memos)
    - other
    
    Reply with just the type name."""
    
    response = llm.invoke(prompt)
    doc_type = response.content.strip().lower()
    print(f"🏷️ Classifier: {doc_type}")
    return {"doc_type": doc_type}


def summarizer_agent(state: DocumentState) -> dict:
    """Stage 3: Create type-appropriate summary."""
    
    # Customize summary style based on document type
    style_guide = {
        "legal": "Focus on parties involved, obligations, and key dates.",
        "medical": "Focus on patient info, diagnosis, and treatment plan.",
        "financial": "Focus on amounts, dates, and financial implications.",
        "correspondence": "Focus on sender, recipient, purpose, and action items.",
        "other": "Focus on main topic, key points, and conclusions."
    }
    
    style = style_guide.get(state["doc_type"], style_guide["other"])
    
    prompt = f"""Summarize this {state['doc_type']} document.
    
    Document: {state['document']}
    
    Key entities: {state['entities']}
    
    Style guide: {style}
    
    Keep summary to 3-4 sentences."""
    
    response = llm.invoke(prompt)
    print("📝 Summarizer complete")
    return {"summary": response.content}


# Build the pipeline
workflow = StateGraph(DocumentState)

workflow.add_node("extractor", extractor_agent)
workflow.add_node("classifier", classifier_agent)
workflow.add_node("summarizer", summarizer_agent)

workflow.add_edge(START, "extractor")
workflow.add_edge("extractor", "classifier")
workflow.add_edge("classifier", "summarizer")
workflow.add_edge("summarizer", END)

app = workflow.compile()

# Test document
sample_doc = """
EMPLOYMENT AGREEMENT

This Agreement is entered into on January 15, 2024, between TechCorp Inc., 
a Delaware corporation located at 100 Innovation Drive, San Francisco, CA 
("Employer"), and Jane Smith ("Employee").

Employee agrees to serve as Senior Software Engineer starting February 1, 2024.
Compensation shall be $150,000 annually, paid bi-weekly. Employee is entitled
to 20 days paid vacation and standard health benefits.

This agreement shall remain in effect for 2 years unless terminated by either
party with 30 days written notice.

Signed: John Davis, CEO, TechCorp Inc.
"""

result = app.invoke({
    "document": sample_doc,
    "entities": "",
    "doc_type": "",
    "summary": ""
})

print("\n" + "=" * 60)
print("DOCUMENT PROCESSING RESULTS")
print("=" * 60)
print(f"\n📋 ENTITIES:\n{result['entities']}")
print(f"\n🏷️ TYPE: {result['doc_type']}")
print(f"\n📝 SUMMARY:\n{result['summary']}")
