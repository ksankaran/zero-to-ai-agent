# From: Zero to AI Agent, Chapter 11, Section 11.6
# File: json_parser.py

from langchain_openai import ChatOpenAI
from langchain_classic.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Define what you want
response_schemas = [
    ResponseSchema(name="title", description="book title"),
    ResponseSchema(name="author", description="book author"),
    ResponseSchema(name="year", description="publication year")
]

# Create parser
parser = StructuredOutputParser.from_response_schemas(response_schemas)

# Create prompt
prompt = PromptTemplate(
    template="Recommend one science fiction book.\n{format_instructions}",
    input_variables=[],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# Run it
llm = ChatOpenAI(temperature=0)
chain = prompt | llm | parser

result = chain.invoke({})
print("Structured data:", result)
print(f"\nTitle: {result['title']}")
print(f"Author: {result['author']}")
print(f"Year: {result['year']}")
