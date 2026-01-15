# From: Building AI Agents, Chapter 14, Section 14.3
# File: verify_api.py

"""Verify API connection is working."""

import os
from dotenv import load_dotenv

def check_api():
    """Check that we can connect to OpenAI."""
    print("🔍 Checking API connection...\n")
    
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        print("   Make sure you have a .env file with your API key")
        return False
    
    if not api_key.startswith("sk-"):
        print("⚠️  API key doesn't start with 'sk-' - it might be invalid")
    
    print("✅ API key found")
    
    # Try to make a simple API call
    print("\n🔄 Testing API connection...")
    
    try:
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        response = llm.invoke("Say 'Hello, LangGraph!' and nothing else.")
        
        print(f"✅ API connection successful!")
        print(f"   Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

if __name__ == "__main__":
    check_api()
