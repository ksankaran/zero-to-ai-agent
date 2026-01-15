# From: Zero to AI Agent, Chapter 11, Section 11.6
# File: safe_parser.py

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class Product(BaseModel):
    name: str = Field(description="product name")
    price: float = Field(description="price in dollars")

parser = PydanticOutputParser(pydantic_object=Product)
llm = ChatOpenAI(temperature=0)

def safe_parse(text: str) -> Product:
    """Parse with error handling"""
    try:
        # Try to parse
        result = parser.parse(text)
        return result
    except Exception as e:
        print(f"Parse failed: {e}")
        print("Attempting to fix...")
        
        # Ask LLM to fix it
        fix_prompt = f"""Fix this JSON to match the required format:
        {text}
        
        Required format: {parser.get_format_instructions()}"""
        
        fixed = llm.invoke(fix_prompt)
        return parser.parse(fixed.content)

# Test with bad JSON
bad_json = '{"name": "Laptop", "price": "one thousand"}'  # price should be number!

result = safe_parse(bad_json)
print(f"Fixed result: {result}")
