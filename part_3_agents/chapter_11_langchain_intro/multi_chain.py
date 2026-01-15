# From: Zero to AI Agent, Chapter 11, Section 11.4
# File: multi_chain.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(temperature=0.7)
parser = StrOutputParser()

# Chain 1: Explain things simply
explain_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms a beginner would understand."
)
explain_chain = explain_prompt | llm | parser

# Chain 2: Generate ideas
idea_prompt = ChatPromptTemplate.from_template(
    "Generate 3 creative ideas for {topic}"
)
idea_chain = idea_prompt | llm | parser

# Use them
explanation = explain_chain.invoke({"topic": "recursion"})
print("Explanation:", explanation[:200], "...\n")

ideas = idea_chain.invoke({"topic": "a birthday party"})
print("Ideas:", ideas[:200], "...")
