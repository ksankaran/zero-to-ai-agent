# From: Zero to AI Agent, Chapter 11, Section 11.6
# File: pydantic_parser.py

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# Define your data model
class Person(BaseModel):
    name: str = Field(description="person's full name")
    age: int = Field(description="age in years")
    occupation: str = Field(description="their job")
    hobby: str = Field(description="favorite hobby")

# Create parser
parser = PydanticOutputParser(pydantic_object=Person)

# Create prompt
prompt = PromptTemplate(
    template="Create a fictional character profile.\n{format_instructions}",
    input_variables=[],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# Run it
llm = ChatOpenAI(temperature=0.7)
chain = prompt | llm | parser

person = chain.invoke({})

# You get a real Python object!
print(f"Name: {person.name}")
print(f"Age: {person.age}")
print(f"Job: {person.occupation}")
print(f"Hobby: {person.hobby}")
