# From: Zero to AI Agent, Chapter 11, Section 11.6
# File: form_extractor.py

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field, validator
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class ContactForm(BaseModel):
    name: str = Field(description="person's full name")
    email: str = Field(description="email address")
    phone: Optional[str] = Field(description="phone number if provided")
    company: Optional[str] = Field(description="company name if mentioned")
    request: str = Field(description="what they want")
    
    @validator('email')
    def email_must_be_valid(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v

parser = PydanticOutputParser(pydantic_object=ContactForm)

prompt = PromptTemplate(
    template="""Extract contact information from this message:

{message}

{format_instructions}""",
    input_variables=["message"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

llm = ChatOpenAI(temperature=0)
chain = prompt | llm | parser

# Test with a real email
email = """
Hi there,

My name is John Smith and I work at TechCorp. You can reach me at 
john.smith@techcorp.com or call me at 555-0123.

I'm interested in getting a demo of your product for our team.

Thanks,
John
"""

contact = chain.invoke({"message": email})

print("Extracted Contact:")
print(f"Name: {contact.name}")
print(f"Email: {contact.email}")
print(f"Phone: {contact.phone}")
print(f"Company: {contact.company}")
print(f"Request: {contact.request}")
