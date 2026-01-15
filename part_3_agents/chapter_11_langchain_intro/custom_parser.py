# From: Zero to AI Agent, Chapter 11, Section 11.6
# File: custom_parser.py

from langchain_core.output_parsers.base import BaseOutputParser
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

class BulletPointParser(BaseOutputParser):
    """Parse bullet points into a list"""
    
    def parse(self, text: str) -> List[str]:
        """Extract bullet points from text"""
        lines = text.split('\n')
        bullet_points = []
        
        for line in lines:
            line = line.strip()
            # Check for various bullet formats
            if line.startswith(('•', '-', '*', '→')):
                # Remove bullet and clean
                clean_line = line[1:].strip()
                bullet_points.append(clean_line)
            elif line and line[0].isdigit() and '.' in line:
                # Numbered list (1. Item)
                parts = line.split('.', 1)
                if len(parts) > 1:
                    bullet_points.append(parts[1].strip())
        
        return bullet_points
    
    def get_format_instructions(self) -> str:
        return "Format your response as a bulleted list using • or - or *"

# Use it
load_dotenv()

parser = BulletPointParser()
prompt = PromptTemplate(
    template="List 3 benefits of {topic}.\n{format_instructions}",
    input_variables=["topic"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

llm = ChatOpenAI()
chain = prompt | llm | parser

benefits = chain.invoke({"topic": "exercise"})
print("Parsed benefits:")
for i, benefit in enumerate(benefits, 1):
    print(f"{i}. {benefit}")
