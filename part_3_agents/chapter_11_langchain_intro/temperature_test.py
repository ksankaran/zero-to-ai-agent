# From: Zero to AI Agent, Chapter 11, Section 11.3
# File: temperature_test.py

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Focused and consistent (temperature = 0)
focused_model = ChatOpenAI(temperature=0)

# Creative and varied (temperature = 1)
creative_model = ChatOpenAI(temperature=1)

prompt = "Write a tagline for a coffee shop"

print("Focused:", focused_model.invoke(prompt).content)
print("Creative:", creative_model.invoke(prompt).content)
