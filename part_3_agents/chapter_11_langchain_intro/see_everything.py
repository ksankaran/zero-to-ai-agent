# From: Zero to AI Agent, Chapter 11, Section 11.7
# File: see_everything.py

from langchain_core.globals import set_debug, set_verbose
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Turn on debug mode
set_debug(True)
set_verbose(True)

# Now run any LangChain code
prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
llm = ChatOpenAI()
chain = prompt | llm

# This will show EVERYTHING
result = chain.invoke({"topic": "debugging"})

# Turn it off when done
set_debug(False)
set_verbose(False)
