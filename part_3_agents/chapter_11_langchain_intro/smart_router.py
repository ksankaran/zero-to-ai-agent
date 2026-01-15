# From: Zero to AI Agent, Chapter 11, Section 11.4
# File: smart_router.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(temperature=0)  # Temperature 0 for consistent routing
parser = StrOutputParser()

# First, classify the request
classifier_prompt = ChatPromptTemplate.from_template(
    """What type of request is this:
    - explain: if user wants explanation
    - create: if user wants ideas or content
    - analyze: if user wants analysis
    
    Request: {request}
    
    Reply with just one word: explain, create, or analyze"""
)

classifier = classifier_prompt | llm | parser

# Test the classifier
request = "Help me understand how photosynthesis works"
request_type = classifier.invoke({"request": request})
print(f"Request: {request}")
print(f"Type detected: {request_type.strip()}")
