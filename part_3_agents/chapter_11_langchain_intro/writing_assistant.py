# From: Zero to AI Agent, Chapter 11, Section 11.3
# File: writing_assistant.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# Create specialized prompts for different improvements
grammar_prompt = ChatPromptTemplate.from_template(
    "Fix any grammar errors in this text. Return only the corrected text:\n{text}"
)

clarity_prompt = ChatPromptTemplate.from_template(
    "Make this text clearer and more concise:\n{text}"
)

tone_prompt = ChatPromptTemplate.from_template(
    "Adjust this text to be more {tone}:\n{text}"
)

# Create the model and parser
model = ChatOpenAI(temperature=0)  # Consistent for editing
parser = StrOutputParser()

# Create chains for each task
grammar_chain = grammar_prompt | model | parser
clarity_chain = clarity_prompt | model | parser
tone_chain = tone_prompt | model | parser

# Test text
text = "The thing is that we should probably maybe consider thinking about it"

# Apply improvements
grammar_fixed = grammar_chain.invoke({"text": text})
print("Grammar fixed:", grammar_fixed)

clarity_improved = clarity_chain.invoke({"text": grammar_fixed})
print("Clarity improved:", clarity_improved)

professional = tone_chain.invoke({"text": clarity_improved, "tone": "professional"})
print("Professional tone:", professional)
