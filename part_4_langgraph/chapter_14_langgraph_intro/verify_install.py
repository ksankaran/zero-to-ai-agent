# From: Building AI Agents, Chapter 14, Section 14.3
# File: verify_install.py

"""Verify that LangGraph is installed correctly."""

def check_installation():
    """Check all required packages."""
    print("🔍 Checking LangGraph installation...\n")
    
    # Check langgraph
    try:
        import langgraph
        print(f"✅ langgraph installed (version: {langgraph.__version__})")
    except ImportError:
        print("❌ langgraph not installed")
        return False
    except AttributeError:
        print("✅ langgraph installed (version not available)")
    
    # Check langchain
    try:
        import langchain
        print(f"✅ langchain installed (version: {langchain.__version__})")
    except ImportError:
        print("❌ langchain not installed")
        return False
    
    # Check langchain-openai
    try:
        from langchain_openai import ChatOpenAI
        print("✅ langchain-openai installed")
    except ImportError:
        print("❌ langchain-openai not installed")
        return False
    
    # Check python-dotenv
    try:
        import dotenv
        print("✅ python-dotenv installed")
    except ImportError:
        print("❌ python-dotenv not installed")
        return False
    
    print("\n🎉 All packages installed correctly!")
    return True

if __name__ == "__main__":
    check_installation()
