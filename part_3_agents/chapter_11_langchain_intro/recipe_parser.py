# From: Zero to AI Agent, Chapter 11, Section 11.6
# File: recipe_parser.py

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Define recipe structure
class Ingredient(BaseModel):
    item: str = Field(description="ingredient name")
    amount: str = Field(description="quantity needed")

class Recipe(BaseModel):
    name: str = Field(description="recipe name")
    cook_time: int = Field(description="minutes to cook")
    difficulty: str = Field(description="easy, medium, or hard")
    ingredients: List[Ingredient] = Field(description="list of ingredients")

# Create parser
parser = PydanticOutputParser(pydantic_object=Recipe)

# Create prompt
prompt = PromptTemplate(
    template="""Create a simple recipe for {dish}.

{format_instructions}""",
    input_variables=["dish"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# Build chain
llm = ChatOpenAI(temperature=0.7)
chain = prompt | llm | parser

# Get structured recipe
recipe = chain.invoke({"dish": "chocolate chip cookies"})

print(f"Recipe: {recipe.name}")
print(f"Time: {recipe.cook_time} minutes")
print(f"Difficulty: {recipe.difficulty}")
print("\nIngredients:")
for ing in recipe.ingredients:
    print(f"  - {ing.amount} {ing.item}")
