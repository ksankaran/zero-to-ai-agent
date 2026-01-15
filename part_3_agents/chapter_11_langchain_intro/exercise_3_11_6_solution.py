# From: Zero to AI Agent, Chapter 11, Section 11.6
# File: exercise_3_11_6_solution.py

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

class ProductReview(BaseModel):
    overall_rating: float = Field(description="Overall rating from 1-5")
    pros: List[str] = Field(description="List of positive aspects")
    cons: List[str] = Field(description="List of negative aspects") 
    would_recommend: bool = Field(description="Whether reviewer would recommend")
    key_features: List[str] = Field(description="Key product features mentioned")
    
    @validator('overall_rating')
    def validate_rating(cls, v):
        if not 1 <= v <= 5:
            raise ValueError('Rating must be between 1 and 5')
        return v

class ReviewExtractor:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0)
        self.parser = PydanticOutputParser(pydantic_object=ProductReview)
        
        self.prompt = PromptTemplate(
            template="""Extract structured information from this product review.

Review:
{review_text}

{format_instructions}

Guidelines:
- Extract rating on 1-5 scale (convert if necessary)
- List specific pros mentioned
- List specific cons mentioned
- Determine if reviewer would recommend based on overall tone
- Identify key product features discussed
""",
            input_variables=["review_text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        self.chain = self.prompt | self.llm | self.parser
    
    def extract(self, review_text):
        """Extract structured data from a review"""
        try:
            result = self.chain.invoke({"review_text": review_text})
            return result
        except Exception as e:
            print(f"Error extracting review data: {e}")
            return None

# Test the extractor
if __name__ == "__main__":
    extractor = ReviewExtractor()
    
    test_review = """
    I bought this wireless headphone last month and I'm giving it 4 stars.
    
    The good: Amazing sound quality with deep bass, comfortable for long wearing,
    excellent battery life (30+ hours), and great noise cancellation. The bluetooth
    connection is stable and the range is impressive.
    
    The not so good: They're quite expensive, the case is bulky for travel,
    and the touch controls can be overly sensitive sometimes.
    
    Overall, despite the high price, I'd recommend these to anyone who values
    audio quality and comfort. The noise cancellation alone makes them worth it
    for frequent travelers or remote workers.
    """
    
    print("📦 Product Review Extractor")
    print("="*60)
    
    result = extractor.extract(test_review)
    if result:
        print(f"Rating: {'⭐' * int(result.overall_rating)} ({result.overall_rating}/5)")
        print(f"\n✅ Pros:")
        for pro in result.pros:
            print(f"  • {pro}")
        print(f"\n❌ Cons:")
        for con in result.cons:
            print(f"  • {con}")
        print(f"\n💡 Would Recommend: {'Yes' if result.would_recommend else 'No'}")
        print(f"\n🔧 Key Features Mentioned:")
        for feature in result.key_features:
            print(f"  • {feature}")
