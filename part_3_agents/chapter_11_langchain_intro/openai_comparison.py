# From: Zero to AI Agent, Chapter 11, Section 11.5
# File: openai_comparison.py

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Create two different models
fast_model = ChatOpenAI(model="gpt-3.5-turbo")
smart_model = ChatOpenAI(model="gpt-4")

# Same prompt, different models
prompt = "Explain why the sky is blue"

fast_response = fast_model.invoke(prompt)
print("GPT-3.5 says:")
print(fast_response.content[:200], "...\n")

smart_response = smart_model.invoke(prompt)
print("GPT-4 says:")
print(smart_response.content[:200], "...")
