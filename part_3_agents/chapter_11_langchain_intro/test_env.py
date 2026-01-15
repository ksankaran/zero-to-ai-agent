# From: Zero to AI Agent, Chapter 11, Section 11.2
# File: test_env.py

import os
from dotenv import load_dotenv

load_dotenv()
print(f"Current directory: {os.getcwd()}")
print(f".env exists: {os.path.exists('.env')}")
print(f"Key loaded: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
