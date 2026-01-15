# From: Zero to AI Agent, Chapter 7, Section 7.6
# File: first_api_call.py

"""
Your first authenticated API calls to real AI services!
Tests connections to OpenAI, Anthropic, and Google Gemini.
"""

import os
from dotenv import load_dotenv
import sys
from typing import Optional, Dict, Any


# Load environment variables from .env file
load_dotenv()


def test_openai() -> bool:
    """
    Test OpenAI API connection with GPT-3.5-Turbo
    
    Returns:
        True if successful, False otherwise
    """
    try:
        from openai import OpenAI
        
        # Get API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "ADD_YOUR_KEY_HERE":
            print("❌ OpenAI: No valid API key found")
            print("   Set OPENAI_API_KEY in your .env file")
            return False
        
        # Initialize client
        client = OpenAI(api_key=api_key)
        
        # Make a simple test call
        print("🔄 Testing OpenAI connection...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Respond with exactly: 'Hello, API world!'"}
            ],
            max_tokens=20,
            temperature=0  # Make response deterministic
        )
        
        # Extract response
        message = response.choices[0].message.content
        print(f"🎉 OpenAI Response: {message}")
        
        # Show token usage
        if hasattr(response, 'usage'):
            print(f"   Tokens used: {response.usage.total_tokens}")
            print(f"   Model: {response.model}")
        
        return True
        
    except ImportError:
        print("❌ OpenAI: Package not installed")
        print("   Run: pip install openai")
        return False
        
    except Exception as e:
        print(f"❌ OpenAI Error: {str(e)[:100]}")
        return False


def test_anthropic() -> bool:
    """
    Test Anthropic API connection with Claude
    
    Returns:
        True if successful, False otherwise
    """
    try:
        from anthropic import Anthropic
        
        # Get API key
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key or api_key == "ADD_YOUR_KEY_HERE":
            print("❌ Anthropic: No valid API key found")
            print("   Set ANTHROPIC_API_KEY in your .env file")
            return False
        
        # Initialize client
        client = Anthropic(api_key=api_key)
        
        # Make a simple test call
        print("🔄 Testing Anthropic connection...")
        message = client.messages.create(
            model="claude-3-haiku-20240307",  # Cheapest Claude model
            max_tokens=20,
            messages=[
                {"role": "user", "content": "Respond with exactly: 'Hello, API world!'"}
            ],
            temperature=0
        )
        
        # Extract response
        response_text = message.content[0].text
        print(f"🎉 Anthropic Response: {response_text}")
        
        # Show usage info
        if hasattr(message, 'usage'):
            print(f"   Tokens used: {message.usage.input_tokens + message.usage.output_tokens}")
        print(f"   Model: {message.model}")
        
        return True
        
    except ImportError:
        print("❌ Anthropic: Package not installed")
        print("   Run: pip install anthropic")
        return False
        
    except Exception as e:
        print(f"❌ Anthropic Error: {str(e)[:100]}")
        return False


def test_google() -> bool:
    """
    Test Google Gemini API connection
    
    Returns:
        True if successful, False otherwise
    """
    try:
        import google.generativeai as genai
        
        # Get API key
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "ADD_YOUR_KEY_HERE":
            print("❌ Google: No valid API key found")
            print("   Set GOOGLE_API_KEY in your .env file")
            return False
        
        # Configure API
        genai.configure(api_key=api_key)
        
        # Create model
        model = genai.GenerativeModel('gemini-pro')
        
        # Make a simple test call
        print("🔄 Testing Google Gemini connection...")
        response = model.generate_content(
            "Respond with exactly: 'Hello, API world!'",
            generation_config=genai.types.GenerationConfig(
                temperature=0,
                max_output_tokens=20,
            )
        )
        
        # Extract response
        print(f"🎉 Google Response: {response.text}")
        print(f"   Model: gemini-pro")
        
        return True
        
    except ImportError:
        print("❌ Google: Package not installed")
        print("   Run: pip install google-generativeai")
        return False
        
    except Exception as e:
        print(f"❌ Google Error: {str(e)[:100]}")
        return False


def test_all_providers() -> Dict[str, bool]:
    """
    Test all configured AI providers
    
    Returns:
        Dictionary with test results for each provider
    """
    results = {}
    
    print("=" * 60)
    print("🚀 Testing AI API Connections")
    print("=" * 60)
    
    # Check which providers have keys configured
    providers = []
    
    if os.getenv("OPENAI_API_KEY"):
        providers.append(("OpenAI", test_openai))
    
    if os.getenv("ANTHROPIC_API_KEY"):
        providers.append(("Anthropic", test_anthropic))
    
    if os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"):
        providers.append(("Google", test_google))
    
    if not providers:
        print("\n⚠️ No API keys configured!")
        print("\nTo get started:")
        print("1. Create a .env file in your project directory")
        print("2. Add your API keys:")
        print("   OPENAI_API_KEY=your-key-here")
        print("   ANTHROPIC_API_KEY=your-key-here")
        print("   GOOGLE_API_KEY=your-key-here")
        return results
    
    # Test each provider
    for name, test_func in providers:
        print(f"\nTesting {name}...")
        print("-" * 40)
        results[name] = test_func()
        print()
    
    return results


def display_summary(results: Dict[str, bool]):
    """Display a summary of test results"""
    
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    if not results:
        print("No providers tested (no API keys configured)")
        return
    
    working = sum(1 for success in results.values() if success)
    total = len(results)
    
    print(f"\nProviders tested: {total}")
    print(f"Working: {working}")
    print(f"Failed: {total - working}")
    
    print("\nDetails:")
    for provider, success in results.items():
        status = "✅ Working" if success else "❌ Failed"
        print(f"  {provider}: {status}")
    
    if working == 0:
        print("\n⚠️ No working API connections!")
        print("\nTroubleshooting steps:")
        print("1. Check that API keys are correctly set in .env")
        print("2. Verify you have credits/billing set up")
        print("3. Install required packages:")
        print("   pip install openai anthropic google-generativeai")
        print("4. Check your internet connection")
    elif working == total:
        print("\n🎉 All API connections working perfectly!")
        print("You're ready to build AI applications!")
    else:
        print(f"\n✅ {working} provider(s) working - enough to get started!")


def check_prerequisites():
    """Check if all prerequisites are met"""
    
    print("Checking prerequisites...")
    print("-" * 40)
    
    # Check for .env file
    if not os.path.exists(".env"):
        print("📝 No .env file found")
        print("Creating template .env file...")
        
        template = """# AI API Keys
# Get your keys from:
# OpenAI: https://platform.openai.com/api-keys
# Anthropic: https://console.anthropic.com/
# Google: https://aistudio.google.com/

OPENAI_API_KEY=ADD_YOUR_KEY_HERE
ANTHROPIC_API_KEY=ADD_YOUR_KEY_HERE
GOOGLE_API_KEY=ADD_YOUR_KEY_HERE
"""
        
        with open(".env", "w") as f:
            f.write(template)
        
        print("✅ Created .env file - please add your API keys")
        return False
    
    # Check for python-dotenv
    try:
        import dotenv
        print("✅ python-dotenv installed")
    except ImportError:
        print("❌ python-dotenv not installed")
        print("   Run: pip install python-dotenv")
        return False
    
    return True


if __name__ == "__main__":
    print("🎯 First API Call - Testing Your AI Connections")
    print("=" * 60)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n⚠️ Please complete setup before testing APIs")
        sys.exit(1)
    
    # Test all providers
    results = test_all_providers()
    
    # Display summary
    display_summary(results)
    
    # Exit code based on results
    if results and any(results.values()):
        sys.exit(0)  # At least one working
    else:
        sys.exit(1)  # None working
