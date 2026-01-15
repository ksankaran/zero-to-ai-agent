# From: Zero to AI Agent, Chapter 17, Section 17.1
# File: setup_check.py

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("✅ OpenAI API key found")
else:
    print("❌ Please set OPENAI_API_KEY in your .env file")

# Test imports
try:
    from langgraph.graph import StateGraph, START, END
    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.types import interrupt, Command
    from langchain_openai import ChatOpenAI
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Run: pip install langgraph langchain-openai python-dotenv")
