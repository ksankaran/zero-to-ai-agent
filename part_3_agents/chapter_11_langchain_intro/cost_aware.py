# From: Zero to AI Agent, Chapter 11, Section 11.5
# File: cost_aware.py

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class CostAwareAssistant:
    def __init__(self):
        # Approximate costs per 1000 tokens
        self.costs = {
            "gpt-3.5-turbo": 0.002,
            "gpt-4": 0.06
        }
        self.budget_used = 0.0
        
    def choose_model(self, importance):
        """Choose model based on importance"""
        if importance == "high":
            model_name = "gpt-4"
            print(f"Using GPT-4 (important question)")
        else:
            model_name = "gpt-3.5-turbo"
            print(f"Using GPT-3.5 (regular question)")
        
        return ChatOpenAI(model=model_name), model_name
    
    def ask(self, question, importance="normal"):
        """Ask with cost awareness"""
        model, model_name = self.choose_model(importance)
        
        # Get response
        response = model.invoke(question)
        
        # Estimate cost (rough calculation)
        tokens = len(question.split()) + len(response.content.split())
        cost = (tokens / 1000) * self.costs[model_name]
        self.budget_used += cost
        
        print(f"Cost: ${cost:.4f} | Total used: ${self.budget_used:.4f}")
        
        return response.content

# Test it
assistant = CostAwareAssistant()

# Normal question - uses cheaper model
print(assistant.ask("What's 2+2?", importance="normal"))

# Important question - uses better model
print(assistant.ask("Explain quantum computing", importance="high"))
