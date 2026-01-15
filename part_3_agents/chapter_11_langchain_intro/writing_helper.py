# From: Zero to AI Agent, Chapter 11, Section 11.4
# File: writing_helper.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Create a simple writing improvement chain
prompt = ChatPromptTemplate.from_template(
    "Improve this text: {text}\n\nMake it clearer and more engaging."
)

llm = ChatOpenAI(temperature=0.7)
chain = prompt | llm

# Test it
text = "The thing is that we should probably consider maybe thinking about it"
result = chain.invoke({"text": text})
print("Original:", text)
print("Improved:", result.content)
