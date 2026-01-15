# From: Zero to AI Agent, Chapter 11, Section 11.5
# File: model_comparison.py

from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from dotenv import load_dotenv
import time

load_dotenv()

def compare_models(question):
    """Compare different models on the same question"""
    
    models = {
        "GPT-3.5": ChatOpenAI(model="gpt-3.5-turbo"),
        "Local": Ollama(model="llama2")
    }
    
    print(f"Question: {question}\n")
    
    for name, model in models.items():
        start = time.time()
        
        try:
            response = model.invoke(question)
            elapsed = time.time() - start
            
            # Get content
            if hasattr(response, 'content'):
                text = response.content
            else:
                text = str(response)
            
            print(f"{name}:")
            print(f"  Time: {elapsed:.2f}s")
            print(f"  Response: {text[:100]}...")
            
        except Exception as e:
            print(f"{name}: Failed - {e}")
        
        print()

# Compare them
compare_models("What makes a good friend?")
