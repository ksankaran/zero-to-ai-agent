# From: Zero to AI Agent, Chapter 11, Section 11.3
# File: exercise_1_11_3_solution.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Create three different prompts for different audiences
technical_prompt = ChatPromptTemplate.from_template(
    """Summarize this text for a technical audience. 
    Include specific details, technical terms, and implementation considerations.
    
    Text: {text}
    
    Technical Summary:"""
)

children_prompt = ChatPromptTemplate.from_template(
    """Explain this text in a way a 10-year-old would understand.
    Use simple words, fun examples, and make it engaging.
    
    Text: {text}
    
    Kid-Friendly Explanation:"""
)

business_prompt = ChatPromptTemplate.from_template(
    """Summarize this text for business executives.
    Focus on impact, ROI, strategic implications, and actionable insights.
    
    Text: {text}
    
    Executive Summary:"""
)

# Test text about AI
test_text = """
Artificial neural networks are computing systems inspired by biological neural networks.
They consist of interconnected nodes that process information using connectionist approaches.
These networks can learn to perform tasks by considering examples, generally without 
being programmed with task-specific rules. They have revolutionized image recognition,
natural language processing, and many other fields.
"""

# Create the model
llm = ChatOpenAI(temperature=0.7)

# Test all three variations
print("Original Text:")
print(test_text)
print("\n" + "="*60 + "\n")

# Technical audience
tech_chain = technical_prompt | llm
tech_result = tech_chain.invoke({"text": test_text})
print("TECHNICAL AUDIENCE:")
print(tech_result.content)
print("\n" + "="*60 + "\n")

# Children audience
children_chain = children_prompt | llm
children_result = children_chain.invoke({"text": test_text})
print("CHILDREN AUDIENCE:")
print(children_result.content)
print("\n" + "="*60 + "\n")

# Business audience
business_chain = business_prompt | llm
business_result = business_chain.invoke({"text": test_text})
print("BUSINESS AUDIENCE:")
print(business_result.content)
