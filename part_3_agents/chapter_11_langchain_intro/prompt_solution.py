# From: Zero to AI Agent, Chapter 11, Section 11.3
# File: prompt_solution.py

from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Create a reusable template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful teacher."),
    ("human", "Teach me about {topic} in simple terms.")
])

# Use it with different inputs
prompt1 = prompt_template.format_messages(topic="recursion")
prompt2 = prompt_template.format_messages(topic="databases")

print("First prompt:", prompt1)
print("\nSecond prompt:", prompt2)
