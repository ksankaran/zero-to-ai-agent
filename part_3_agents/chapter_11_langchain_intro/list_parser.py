# From: Zero to AI Agent, Chapter 11, Section 11.6
# File: list_parser.py

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Create a list parser
parser = CommaSeparatedListOutputParser()

# Create prompt with parser instructions
prompt = PromptTemplate(
    template="List 5 {category}.\n{format_instructions}",
    input_variables=["category"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# Chain it together
llm = ChatOpenAI(temperature=0)
chain = prompt | llm | parser

# Get a real Python list!
result = chain.invoke({"category": "programming languages"})
print("Result type:", type(result))
print("Result:", result)

# Now you can use it like any list
for i, lang in enumerate(result, 1):
    print(f"{i}. {lang}")
