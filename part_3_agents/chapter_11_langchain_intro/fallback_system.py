# From: Zero to AI Agent, Chapter 11, Section 11.5
# File: fallback_system.py

from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from dotenv import load_dotenv

load_dotenv()

class ResilientAssistant:
    def __init__(self):
        # Primary model
        self.primary = ChatOpenAI(model="gpt-3.5-turbo")
        
        # Fallback model (local)
        self.fallback = Ollama(model="llama2")
    
    def ask(self, question):
        """Try primary, fall back if needed"""
        try:
            print("Trying primary model...")
            response = self.primary.invoke(question)
            return response.content
        except Exception as e:
            print(f"Primary failed: {e}")
            print("Using fallback model...")
            response = self.fallback.invoke(question)
            return str(response)

# Test it
assistant = ResilientAssistant()
answer = assistant.ask("What is resilience?")
print("Answer:", answer[:200], "...")
