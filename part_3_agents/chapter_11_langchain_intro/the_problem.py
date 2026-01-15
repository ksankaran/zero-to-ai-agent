# From: Zero to AI Agent, Chapter 11, Section 11.6
# File: the_problem.py

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(temperature=0)

# Ask for structured data
response = llm.invoke("""
List 3 books with title, author, and year.
""")

print("AI Response:")
print(response.content)
print("\n" + "="*50)
print("Problem: How do we extract this data reliably?")
