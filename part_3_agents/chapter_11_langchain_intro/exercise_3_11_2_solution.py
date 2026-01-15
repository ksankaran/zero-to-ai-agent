# From: Zero to AI Agent, Chapter 11, Section 11.2
# File: exercise_3_11_2_solution.py

import os
import sys
import time
from dotenv import load_dotenv

def test_connection():
    """Comprehensive connection testing with fixes"""
    
    print("🔌 LangChain Connection Tester")
    print("=" * 40)
    
    # Step 1: Check environment
    print("\n1️⃣ Checking environment setup...")
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No API key found")
        print("\n💡 Fix:")
        print("   1. Create a .env file in this directory")
        print("   2. Add: OPENAI_API_KEY=sk-...")
        print("   3. Get key from: https://platform.openai.com/api-keys")
        return False
    
    print(f"✅ API key found ({len(api_key)} chars)")
    
    # Step 2: Check imports
    print("\n2️⃣ Checking LangChain installation...")
    try:
        from langchain_openai import ChatOpenAI
        print("✅ LangChain imports successful")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("\n💡 Fix:")
        print("   Run: pip install langchain langchain-openai")
        return False
    
    # Step 3: Test connection
    print("\n3️⃣ Testing OpenAI connection...")
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo")
        
        # Simple test query
        start = time.time()
        response = llm.invoke("Say 'Connection successful!'")
        elapsed = time.time() - start
        
        print(f"✅ Connection successful! (Response in {elapsed:.2f}s)")
        print(f"   Response: {response.content}")
        return True
        
    except Exception as e:
        error_msg = str(e).lower()
        print(f"❌ Connection failed: {e}")
        
        # Provide specific fixes based on error
        print("\n💡 Suggested fixes:")
        
        if "api" in error_msg and "key" in error_msg:
            print("   • Check if your API key is valid")
            print("   • Ensure key starts with 'sk-'")
            print("   • Try generating a new key")
            
        elif "rate" in error_msg:
            print("   • You've hit rate limits")
            print("   • Wait a few minutes and try again")
            print("   • Consider upgrading your OpenAI plan")
            
        elif "connection" in error_msg or "network" in error_msg:
            print("   • Check your internet connection")
            print("   • Try disabling VPN if using one")
            print("   • Check if OpenAI is accessible from your location")
            
        elif "model" in error_msg:
            print("   • The model name might be incorrect")
            print("   • Try using 'gpt-3.5-turbo' or 'gpt-4'")
            
        else:
            print("   • Check OpenAI service status")
            print("   • Ensure you have credits in your account")
            print("   • Try updating LangChain: pip install -U langchain")
        
        return False
    
    finally:
        print("\n" + "=" * 40)
        print("Testing complete")

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
