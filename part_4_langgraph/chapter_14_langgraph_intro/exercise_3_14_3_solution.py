# From: Building AI Agents, Chapter 14, Section 14.3
# File: exercise_3_14_3_solution.py (Comprehensive Setup Checker)

"""Comprehensive setup verification for LangGraph development."""

import sys

def print_header(title):
    """Print a formatted section header."""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print('='*50)

def check_python_version():
    """Check Python version is 3.9+."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} (need 3.9+)")
        return False

def check_packages():
    """Check all required packages are installed."""
    packages = {
        'langgraph': 'langgraph',
        'langchain': 'langchain', 
        'langchain_openai': 'langchain-openai',
        'dotenv': 'python-dotenv'
    }
    
    all_good = True
    for import_name, package_name in packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - run: pip install {package_name}")
            all_good = False
    
    return all_good

def check_api_key():
    """Check API key is configured."""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found")
        print("   Create a .env file with: OPENAI_API_KEY=sk-...")
        return False
    
    if not api_key.startswith("sk-"):
        print("⚠️  API key format looks wrong (should start with 'sk-')")
        return False
    
    # Mask the key for display
    masked = api_key[:7] + "..." + api_key[-4:]
    print(f"✅ API key found ({masked})")
    return True

def check_api_connection():
    """Test actual API connection."""
    try:
        from langchain_openai import ChatOpenAI
        
        print("🔄 Testing API connection...")
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=10)
        response = llm.invoke("Say 'OK'")
        print(f"✅ API connection working")
        return True
        
    except Exception as e:
        error_msg = str(e)
        if "authentication" in error_msg.lower():
            print("❌ API authentication failed - check your key")
        elif "rate" in error_msg.lower():
            print("❌ Rate limited - wait a minute and try again")
        elif "quota" in error_msg.lower():
            print("❌ No API quota - add credits to your OpenAI account")
        else:
            print(f"❌ API error: {error_msg[:100]}")
        return False

def check_langgraph_imports():
    """Check LangGraph components are importable."""
    try:
        from langgraph.graph import StateGraph, END
        from langgraph.checkpoint.memory import MemorySaver
        print("✅ LangGraph components accessible")
        return True
    except ImportError as e:
        print(f"❌ LangGraph import failed: {e}")
        return False

def main():
    """Run all checks and report results."""
    print("\n🔍 LangGraph Setup Checker")
    print("=" * 50)
    
    results = {}
    
    # Check Python
    print_header("Python Version")
    results['python'] = check_python_version()
    
    # Check packages
    print_header("Required Packages")
    results['packages'] = check_packages()
    
    # Check LangGraph imports
    print_header("LangGraph Components")
    results['langgraph'] = check_langgraph_imports()
    
    # Check API key
    print_header("API Configuration")
    results['api_key'] = check_api_key()
    
    # Check API connection (only if key exists)
    if results['api_key']:
        print_header("API Connection Test")
        results['api_connection'] = check_api_connection()
    else:
        results['api_connection'] = False
    
    # Summary
    print_header("Summary")
    
    all_passed = all(results.values())
    passed = sum(results.values())
    total = len(results)
    
    for check, result in results.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check.replace('_', ' ').title()}")
    
    print(f"\n  Result: {passed}/{total} checks passed")
    
    if all_passed:
        print("\n🎉 All checks passed! You're ready to build with LangGraph!")
    else:
        print("\n⚠️  Some checks failed. Fix the issues above and run again.")
        print("   Need help? Check the troubleshooting section in 14.3")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
