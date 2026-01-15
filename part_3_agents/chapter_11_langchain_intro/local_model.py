# From: Zero to AI Agent, Chapter 11, Section 11.5
# File: local_model.py

from langchain_community.llms import Ollama

# No API key needed!
local_model = Ollama(model="llama2")

# Works offline!
response = local_model.invoke("Why is privacy important?")
print("Local model says:", response)
