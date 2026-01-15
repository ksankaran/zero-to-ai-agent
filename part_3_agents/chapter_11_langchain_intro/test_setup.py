# From: Zero to AI Agent, Chapter 11, Section 11.2
# File: test_setup.py

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Check if API key loaded
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("✅ API key loaded!")
    print(f"   Key starts with: {api_key[:7]}...")
else:
    print("❌ No API key found")
