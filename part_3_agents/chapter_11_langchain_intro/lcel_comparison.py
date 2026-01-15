# From: Zero to AI Agent, Chapter 11, Section 11.3
# File: lcel_comparison.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

prompt = ChatPromptTemplate.from_template("Translate to French: {text}")
model = ChatOpenAI()

# The OLD way (still works but verbose)
old_chain = LLMChain(llm=model, prompt=prompt)
old_result = old_chain.run(text="Hello world")
print("Old way:", old_result)

# The NEW way with LCEL (clean and intuitive!)
new_chain = prompt | model
new_result = new_chain.invoke({"text": "Hello world"})
print("New way:", new_result.content)
