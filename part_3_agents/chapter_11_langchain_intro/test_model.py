# From: Zero to AI Agent, Chapter 11, Section 11.3
# File: test_model.py

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Create a model instance
model = ChatOpenAI(model="gpt-3.5-turbo")

# Use it (same interface for ALL models!)
response = model.invoke("Hello, AI!")
print(response.content)
