# From: Zero to AI Agent, Chapter 11, Section 11.3
# File: simple_chain.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Create components
prompt = ChatPromptTemplate.from_template(
    "Tell me a joke about {topic}"
)
model = ChatOpenAI()

# Connect them with a chain (using the pipe operator!)
chain = prompt | model

# Run the chain
result = chain.invoke({"topic": "programming"})
print(result.content)
