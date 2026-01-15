# From: Zero to AI Agent, Chapter 11, Section 11.3
# File: chain_composition.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Component 1: Idea generator
idea_prompt = ChatPromptTemplate.from_template(
    "Generate a creative name for a {type} business"
)

# Component 2: Slogan creator
slogan_prompt = ChatPromptTemplate.from_template(
    "Create a catchy slogan for a business called: {name}"
)

model = ChatOpenAI(temperature=0.7)

# Create individual chains
idea_chain = idea_prompt | model
slogan_chain = slogan_prompt | model

# Use them together (manually for now)
business_type = "coffee shop"

# Generate name
name_response = idea_chain.invoke({"type": business_type})
business_name = name_response.content

print(f"Business name: {business_name}")

# Generate slogan
slogan_response = slogan_chain.invoke({"name": business_name})
print(f"Slogan: {slogan_response.content}")
