# From: Zero to AI Agent, Chapter 17, Section 17.2
# Save as: setup_streaming.py

import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Verify setup
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("✅ OpenAI API key found")
else:
    print("❌ Please set OPENAI_API_KEY in your .env file")

# Test imports
try:
    from langgraph.graph import StateGraph, START, END
    from langchain_openai import ChatOpenAI
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
