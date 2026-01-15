# From: Zero to AI Agent, Chapter 11, Section 11.2
# File: exercise_1_11_2_solution.py

import sys
import os
import subprocess
from dotenv import load_dotenv

def generate_environment_report():
    """Generate a comprehensive environment report"""
    
    load_dotenv()
    
    print("=" * 60)
    print("🔍 ENVIRONMENT REPORT")
    print("=" * 60)
    
    # Python version
    print(f"\n📌 Python Version: {sys.version}")
    print(f"   Executable: {sys.executable}")
    
    # LangChain version
    try:
        import langchain
        print(f"\n📦 LangChain Version: {langchain.__version__}")
    except ImportError:
        print("\n❌ LangChain not installed")
    
    # API Key check (without revealing it)
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"\n🔑 OpenAI API Key: Present ({len(api_key)} characters)")
        print(f"   Starts with: {api_key[:7]}...")
    else:
        print("\n❌ OpenAI API Key: Not found")
    
    # Current working directory
    print(f"\n📁 Current Directory: {os.getcwd()}")
    
    # Check if .env file exists
    if os.path.exists(".env"):
        print("   ✅ .env file found")
    else:
        print("   ❌ .env file not found")
    
    # List key packages
    print("\n📚 Key Packages Installed:")
    key_packages = ["langchain", "langchain-openai", "langchain-community", 
                   "openai", "python-dotenv"]
    
    for package in key_packages:
        try:
            result = subprocess.run(
                ["pip", "show", package],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.startswith('Version:'):
                        version = line.split(':')[1].strip()
                        print(f"   ✅ {package}: {version}")
                        break
            else:
                print(f"   ❌ {package}: Not installed")
        except Exception:
            print(f"   ⚠️  {package}: Could not check")
    
    print("\n" + "=" * 60)
    print("Report complete! Save this when things are working.")
    print("=" * 60)

if __name__ == "__main__":
    generate_environment_report()
