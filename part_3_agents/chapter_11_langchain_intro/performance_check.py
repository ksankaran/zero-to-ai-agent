# From: Zero to AI Agent, Chapter 11, Section 11.7
# File: performance_check.py

import time
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def time_operation(name, func):
    """Time any operation"""
    start = time.time()
    result = func()
    elapsed = time.time() - start
    print(f"{name}: {elapsed:.2f} seconds")
    return result

# Test different parts
prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
llm = ChatOpenAI()

# Time prompt formatting
def format_prompt():
    return prompt.format_messages(topic="testing")

# Time LLM call
def call_llm():
    return llm.invoke("Quick test")

# Time full chain
def run_chain():
    chain = prompt | llm
    return chain.invoke({"topic": "speed"})

print("Performance Analysis:")
time_operation("Prompt formatting", format_prompt)
time_operation("LLM call", call_llm)
time_operation("Full chain", run_chain)
