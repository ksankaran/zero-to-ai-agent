# From: Zero to AI Agent, Chapter 11, Section 11.6
# File: exercise_2_11_6_solution.py

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

class ActionItem(BaseModel):
    task: str = Field(description="The task to be completed")
    owner: str = Field(description="Person responsible")
    deadline: Optional[str] = Field(description="When it's due")

class MeetingMinutes(BaseModel):
    meeting_date: str = Field(description="Date of the meeting")
    attendees: List[str] = Field(description="List of attendees")
    key_decisions: List[str] = Field(description="Key decisions made")
    action_items: List[ActionItem] = Field(description="Action items with owners")
    follow_up_dates: List[str] = Field(description="Follow-up dates mentioned")
    main_topics: List[str] = Field(description="Main topics discussed")
    
    @validator('attendees')
    def validate_attendees(cls, v):
        if not v:
            raise ValueError('At least one attendee required')
        return v

class MeetingNotesParser:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0)
        self.parser = PydanticOutputParser(pydantic_object=MeetingMinutes)
        
        self.prompt = PromptTemplate(
            template="""Extract structured information from these meeting notes.

Meeting Notes:
{notes}

{format_instructions}

Focus on:
- All people mentioned as attendees
- Clear decisions (look for "decided", "agreed", "will")
- Action items with specific owners
- Any follow-up dates or deadlines
""",
            input_variables=["notes"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        self.chain = self.prompt | self.llm | self.parser
    
    def parse(self, notes_text):
        """Parse meeting notes"""
        try:
            result = self.chain.invoke({"notes": notes_text})
            return result
        except Exception as e:
            print(f"Error parsing notes: {e}")
            return None

# Test the parser
if __name__ == "__main__":
    parser = MeetingNotesParser()
    
    test_notes = """
    Team Meeting - March 15, 2024
    
    Attendees: Alice Johnson (PM), Bob Chen (Dev Lead), Carol White (Designer)
    
    Discussion:
    - Reviewed Q2 product roadmap
    - Discussed user feedback from beta testing
    - Decided to prioritize mobile app improvements
    - Agreed on new feature freeze date: April 1st
    
    Action Items:
    - Alice: Schedule stakeholder review by March 20
    - Bob: Complete API documentation by March 25
    - Carol: Deliver new mockups by March 22
    
    Follow-up meeting scheduled for March 29 to review progress.
    """
    
    print("📝 Meeting Notes Parser")
    print("="*60)
    
    result = parser.parse(test_notes)
    if result:
        print(f"Date: {result.meeting_date}")
        print(f"Attendees: {', '.join(result.attendees)}")
        print(f"\nKey Decisions:")
        for decision in result.key_decisions:
            print(f"  • {decision}")
        print(f"\nAction Items:")
        for item in result.action_items:
            print(f"  • {item.task}")
            print(f"    Owner: {item.owner}")
            if item.deadline:
                print(f"    Due: {item.deadline}")
        print(f"\nFollow-up Dates: {', '.join(result.follow_up_dates)}")
