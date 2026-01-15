# From: Zero to AI Agent, Chapter 17, Section 17.2
# Save as: exercise_3_17_2_solution.py
# Exercise 3: Multi-Step Form Validator

import asyncio
import re
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import StreamWriter
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class FormState(TypedDict):
    form_data: dict
    validation_results: dict
    address_analysis: str
    is_valid: bool
    status: str

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3, streaming=True)

def validate_email(email: str) -> tuple[bool, str]:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, "Valid email format"
    return False, "Invalid email format"

def validate_phone(phone: str) -> tuple[bool, str]:
    """Validate phone number format."""
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)\.]', '', phone)
    if len(cleaned) >= 10 and cleaned.isdigit():
        return True, "Valid phone format"
    return False, "Invalid phone format (need at least 10 digits)"

def validate_name(name: str) -> tuple[bool, str]:
    """Validate name."""
    if len(name.strip()) >= 2:
        return True, "Valid name"
    return False, "Name must be at least 2 characters"

async def validate_basic_fields(state: FormState, writer: StreamWriter) -> dict:
    """Validate name, email, and phone fields."""
    
    form = state["form_data"]
    results = {}
    
    # Validate name
    writer({"field": "name", "status": "validating", "message": "Validating name..."})
    await asyncio.sleep(0.3)
    valid, msg = validate_name(form.get("name", ""))
    results["name"] = {"valid": valid, "message": msg}
    icon = "✅" if valid else "❌"
    writer({"field": "name", "status": "complete", "message": f"{icon} Name: {msg}"})
    
    # Validate email
    writer({"field": "email", "status": "validating", "message": "Validating email..."})
    await asyncio.sleep(0.3)
    valid, msg = validate_email(form.get("email", ""))
    results["email"] = {"valid": valid, "message": msg}
    icon = "✅" if valid else "❌"
    writer({"field": "email", "status": "complete", "message": f"{icon} Email: {msg}"})
    
    # Validate phone
    writer({"field": "phone", "status": "validating", "message": "Validating phone..."})
    await asyncio.sleep(0.3)
    valid, msg = validate_phone(form.get("phone", ""))
    results["phone"] = {"valid": valid, "message": msg}
    icon = "✅" if valid else "❌"
    writer({"field": "phone", "status": "complete", "message": f"{icon} Phone: {msg}"})
    
    return {"validation_results": results, "status": "basic_validated"}

async def validate_address_with_llm(state: FormState, writer: StreamWriter) -> dict:
    """Use LLM to analyze if the address looks valid."""
    
    address = state["form_data"].get("address", "")
    
    writer({
        "field": "address",
        "status": "analyzing",
        "message": "🤖 Analyzing address with AI..."
    })
    
    prompt = f"""Analyze this address and determine if it looks like a valid, complete address:

Address: {address}

Check for:
1. Street number and name
2. City
3. State/Province
4. Postal/ZIP code
5. Country (if applicable)

Respond with:
- VALID or INVALID
- Brief explanation (1-2 sentences)
- What's missing if invalid"""
    
    response = await llm.ainvoke(prompt)
    analysis = response.content
    
    # Determine validity from response
    is_valid = "VALID" in analysis.upper() and "INVALID" not in analysis.upper()
    
    # Update validation results
    results = state["validation_results"].copy()
    results["address"] = {
        "valid": is_valid,
        "message": "Address looks valid" if is_valid else "Address may be incomplete"
    }
    
    icon = "✅" if is_valid else "❌"
    writer({
        "field": "address",
        "status": "complete",
        "message": f"{icon} Address validated"
    })
    
    return {
        "validation_results": results,
        "address_analysis": analysis,
        "status": "address_validated"
    }

async def compile_results(state: FormState, writer: StreamWriter) -> dict:
    """Compile all validation results."""
    
    writer({"status": "compiling", "message": "\n📋 Compiling validation results..."})
    await asyncio.sleep(0.2)
    
    results = state["validation_results"]
    all_valid = all(r["valid"] for r in results.values())
    
    return {"is_valid": all_valid, "status": "complete"}

def build_validator_graph():
    workflow = StateGraph(FormState)
    
    workflow.add_node("validate_basic", validate_basic_fields)
    workflow.add_node("validate_address", validate_address_with_llm)
    workflow.add_node("compile", compile_results)
    
    workflow.add_edge(START, "validate_basic")
    workflow.add_edge("validate_basic", "validate_address")
    workflow.add_edge("validate_address", "compile")
    workflow.add_edge("compile", END)
    
    return workflow.compile()

async def stream_address_analysis(graph, state: dict):
    """Stream the LLM's address analysis token-by-token."""
    
    print("\n🤖 AI Address Analysis:")
    print("-" * 40)
    
    async for event in graph.astream_events(state, version="v2"):
        if event["event"] == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            if hasattr(chunk, "content") and chunk.content:
                print(chunk.content, end="", flush=True)
    
    print("\n" + "-" * 40)

async def run_form_validator():
    """Run the form validator with streaming feedback."""
    
    graph = build_validator_graph()
    
    # Sample form data (you could make this interactive)
    print("📝 Form Validator")
    print("=" * 60)
    print("Enter form data (or press Enter for defaults):\n")
    
    name = input("Name [John Doe]: ").strip() or "John Doe"
    email = input("Email [john@example.com]: ").strip() or "john@example.com"
    phone = input("Phone [555-123-4567]: ").strip() or "555-123-4567"
    address = input("Address [123 Main St, Springfield, IL 62701]: ").strip() or "123 Main St, Springfield, IL 62701"
    
    form_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "address": address
    }
    
    initial_state = {
        "form_data": form_data,
        "validation_results": {},
        "address_analysis": "",
        "is_valid": False,
        "status": "starting"
    }
    
    print("\n" + "=" * 60)
    print("🔍 Validating form fields...\n")
    
    final_results = {}
    address_analysis = ""
    is_valid = False
    
    # Stream validation progress
    async for mode, chunk in graph.astream(
        initial_state,
        stream_mode=["updates", "custom"]
    ):
        if mode == "custom":
            status = chunk.get("status", "")
            message = chunk.get("message", "")
            
            if status == "validating":
                print(f"  ⏳ {message}")
            elif status in ["complete", "analyzing", "compiling"]:
                print(f"  {message}")
                
        elif mode == "updates":
            for node_name, updates in chunk.items():
                if "validation_results" in updates:
                    final_results = updates["validation_results"]
                if "address_analysis" in updates:
                    address_analysis = updates["address_analysis"]
                if "is_valid" in updates:
                    is_valid = updates["is_valid"]
    
    # Display final results
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("-" * 60)
    
    for field, result in final_results.items():
        icon = "✅" if result["valid"] else "❌"
        print(f"  {icon} {field.capitalize()}: {result['message']}")
    
    print("-" * 60)
    
    if address_analysis:
        print("\n🤖 AI Address Analysis:")
        print(address_analysis)
    
    print("\n" + "-" * 60)
    
    if is_valid:
        print("✅ FORM IS VALID - Ready to submit!")
    else:
        print("❌ FORM HAS ERRORS - Please fix the issues above")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_form_validator())
