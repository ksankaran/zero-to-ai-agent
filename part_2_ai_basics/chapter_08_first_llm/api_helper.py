# From: Zero to AI Agent, Chapter 8, Section 8.5
# File: api_helper.py

"""Helper functions for API setup"""

from pathlib import Path
import openai

def get_client():
    """Load API key and return OpenAI client"""
    env_file = Path(".env")
    if not env_file.exists():
        raise FileNotFoundError("No .env file found! Please create one with your API key.")
    
    with open(env_file, 'r') as f:
        for line in f:
            if line.startswith('OPENAI_API_KEY='):
                api_key = line.split('=')[1].strip()
                return openai.OpenAI(api_key=api_key)
    
    raise ValueError("No OPENAI_API_KEY found in .env file!")
