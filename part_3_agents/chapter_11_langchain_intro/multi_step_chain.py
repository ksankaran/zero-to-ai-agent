# From: Zero to AI Agent, Chapter 11, Section 11.3
# File: multi_step_chain.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# Step 1: Generate a story
story_prompt = ChatPromptTemplate.from_template(
    "Write a 2-sentence story about {animal}"
)

# Step 2: Extract the moral
moral_prompt = ChatPromptTemplate.from_template(
    "What's the moral of this story: {story}"
)

model = ChatOpenAI()
output_parser = StrOutputParser()  # Extracts just the text

# Build the chain
story_chain = story_prompt | model | output_parser
moral_chain = moral_prompt | model | output_parser

# Run both steps
story = story_chain.invoke({"animal": "ant"})
print("Story:", story)

moral = moral_chain.invoke({"story": story})
print("\nMoral:", moral)
