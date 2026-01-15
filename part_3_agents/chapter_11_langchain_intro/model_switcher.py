# From: Zero to AI Agent, Chapter 11, Section 11.5
# File: model_switcher.py

from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from dotenv import load_dotenv

load_dotenv()

class ModelSwitcher:
    def __init__(self):
        # Initialize available models
        self.models = {
            "fast": ChatOpenAI(model="gpt-3.5-turbo"),
            "smart": ChatOpenAI(model="gpt-4"),
            "local": Ollama(model="llama2")
        }
        self.current = "fast"
    
    def switch_to(self, model_name):
        """Switch to a different model"""
        if model_name in self.models:
            self.current = model_name
            return f"Switched to {model_name}"
        return "Model not available"
    
    def ask(self, question):
        """Ask current model"""
        model = self.models[self.current]
        response = model.invoke(question)
        
        # Handle different response types
        if hasattr(response, 'content'):
            return response.content
        else:
            return str(response)

# Test it
switcher = ModelSwitcher()

question = "What is happiness?"

for model_name in ["fast", "smart", "local"]:
    switcher.switch_to(model_name)
    print(f"\n{model_name.upper()} model:")
    print(switcher.ask(question)[:150], "...")
