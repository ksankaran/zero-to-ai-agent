# From: Zero to AI Agent, Chapter 11, Section 11.7
# File: common_problems.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

def debug_api_key():
    """Check if API key is loaded"""
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("❌ No API key found!")
        print("Fix: Check your .env file")
    else:
        print(f"✅ API key loaded: {key[:7]}...")

def debug_chain_error():
    """Debug a broken chain"""
    try:
        # Intentionally broken chain
        prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
        llm = ChatOpenAI()
        chain = prompt | llm
        
        # Missing required variable!
        result = chain.invoke({})  # No 'topic' provided
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Fix: Check all required variables are provided")

def debug_model_response():
    """Debug unexpected model responses"""
    llm = ChatOpenAI(temperature=0)
    
    # Add system message for consistency
    from langchain_classic.schema import SystemMessage, HumanMessage
    
    messages = [
        SystemMessage(content="You are a helpful assistant. Always respond with exactly 'OK' to test messages."),
        HumanMessage(content="This is a test")
    ]
    
    response = llm.invoke(messages)
    
    if response.content.strip() == "OK":
        print("✅ Model responding correctly")
    else:
        print(f"❌ Unexpected response: {response.content}")
        print("Fix: Check temperature, prompts, and model settings")

# Run all checks
print("Running diagnostics...\n")
debug_api_key()
debug_chain_error()
debug_model_response()
