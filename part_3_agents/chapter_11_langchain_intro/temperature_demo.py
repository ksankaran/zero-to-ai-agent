# From: Zero to AI Agent, Chapter 11, Section 11.5
# File: temperature_demo.py

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Temperature controls creativity
focused_model = ChatOpenAI(temperature=0)    # Consistent, focused
balanced_model = ChatOpenAI(temperature=0.5)  # Balanced
creative_model = ChatOpenAI(temperature=1)    # Creative, varied

prompt = "Write a tagline for a coffee shop"

print("Focused (temp=0):", focused_model.invoke(prompt).content)
print("Balanced (temp=0.5):", balanced_model.invoke(prompt).content)
print("Creative (temp=1):", creative_model.invoke(prompt).content)
