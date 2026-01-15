# From: Zero to AI Agent, Chapter 11, Section 11.6
# File: exercise_1_11_6_solution.py

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

class EmailDetails(BaseModel):
    sender_name: str = Field(description="Sender's full name")
    sender_email: str = Field(description="Sender's email address")
    sender_company: Optional[str] = Field(description="Sender's company if mentioned")
    email_category: str = Field(description="Category: support, sales, or complaint")
    sentiment: str = Field(description="Sentiment: positive, negative, or neutral")
    action_required: bool = Field(description="Whether action is required")
    priority_level: str = Field(description="Priority: high, medium, or low")
    
    @validator('email_category')
    def validate_category(cls, v):
        if v not in ['support', 'sales', 'complaint']:
            raise ValueError('Category must be support, sales, or complaint')
        return v
    
    @validator('sentiment')
    def validate_sentiment(cls, v):
        if v not in ['positive', 'negative', 'neutral']:
            raise ValueError('Sentiment must be positive, negative, or neutral')
        return v
    
    @validator('priority_level')
    def validate_priority(cls, v):
        if v not in ['high', 'medium', 'low']:
            raise ValueError('Priority must be high, medium, or low')
        return v

class EmailAnalyzer:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0)
        self.parser = PydanticOutputParser(pydantic_object=EmailDetails)
        
        self.prompt = PromptTemplate(
            template="""Analyze this email and extract the requested information.

Email:
{email_text}

{format_instructions}

Use these guidelines:
- Support: asking for help or reporting issues
- Sales: inquiring about products or services
- Complaint: expressing dissatisfaction
- High priority: urgent issues or from important senders
- Action required: needs a response or follow-up
""",
            input_variables=["email_text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        self.chain = self.prompt | self.llm | self.parser
    
    def analyze(self, email_text):
        """Analyze an email and extract structured information"""
        try:
            result = self.chain.invoke({"email_text": email_text})
            return result
        except Exception as e:
            print(f"Error analyzing email: {e}")
            return None

# Test the analyzer
if __name__ == "__main__":
    analyzer = EmailAnalyzer()
    
    test_email = """
    From: Jane Smith <jane.smith@techcorp.com>
    Subject: Urgent: System not working properly
    
    Hello Support Team,
    
    I'm experiencing critical issues with your software. Our entire team 
    at TechCorp cannot access the dashboard since this morning. This is 
    blocking our work and we need immediate assistance.
    
    Please help us resolve this as soon as possible.
    
    Best regards,
    Jane Smith
    Senior Manager, TechCorp
    """
    
    print("📧 Email Analyzer")
    print("="*60)
    
    result = analyzer.analyze(test_email)
    if result:
        print(f"Sender: {result.sender_name} ({result.sender_email})")
        print(f"Company: {result.sender_company}")
        print(f"Category: {result.email_category}")
        print(f"Sentiment: {result.sentiment}")
        print(f"Action Required: {result.action_required}")
        print(f"Priority: {result.priority_level}")
