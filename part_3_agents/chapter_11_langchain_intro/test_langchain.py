# From: Zero to AI Agent, Chapter 11, Section 11.2
# File: test_langchain.py

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()

# Create the simplest possible chain
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Test it
response = llm.invoke("Say 'LangChain is working!'")
print(response.content)
