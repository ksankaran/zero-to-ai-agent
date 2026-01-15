# From: Zero to AI Agent, Chapter 12, Section 12.5
# File: exercise_2_12_5_solution.py

from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

# Track calls to detect loops
clarification_count = 0
MAX_CLARIFICATIONS = 1  # Prevent loops

def question_answering(question: str) -> str:
    """Answer questions directly."""
    # Simple Q&A logic
    if "python" in question.lower():
        return "Python is a high-level programming language known for simplicity."
    return f"Here's the answer to '{question}': [detailed answer]"

def ask_clarification(topic: str) -> str:
    """Ask for clarification - potential loop risk!"""
    global clarification_count
    clarification_count += 1
    
    # LOOP PREVENTION: Stop after one clarification
    if clarification_count > MAX_CLARIFICATIONS:
        return "Proceeding with available information."
    
    return f"Could you be more specific about '{topic}'?"

def get_definition(term: str) -> str:
    """Get definition of a term."""
    definitions = {
        "python": "A programming language",
        "api": "Application Programming Interface",
        "llm": "Large Language Model"
    }
    return definitions.get(term.lower(), f"Definition of {term}: [standard definition]")

# Create tools with loop prevention in descriptions
tools = [
    Tool(
        name="answer_question",
        func=question_answering,
        description="Answer questions directly. Always try this first."
    ),
    Tool(
        name="clarify",
        func=ask_clarification,
        description="Ask for clarification ONLY if absolutely needed. Maximum once per conversation."
    ),
    Tool(
        name="define",
        func=get_definition,
        description="Get definition of technical terms"
    )
]

# Test with LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# Test queries
test_queries = [
    "What is Python?",
    "Tell me about programming",
    "Define API"
]

print("LOOP PREVENTION DEMONSTRATION")
print("=" * 50)

for query in test_queries:
    clarification_count = 0  # Reset for each query
    print(f"\nQuery: '{query}'")
    
    response = llm_with_tools.invoke([HumanMessage(content=query)])
    if response.tool_calls:
        tool_name = response.tool_calls[0]['name']
        print(f"Tool selected: {tool_name}")
        
        # Execute tool
        tool = next(t for t in tools if t.name == tool_name)
        result = tool.func(query)
        print(f"Result: {result}")
        
        if tool_name == "clarify":
            print(f"Clarification count: {clarification_count}/{MAX_CLARIFICATIONS}")

print("\n✅ Loop Prevention Strategies Applied:")
print("1. Clarification limited to once per query")
print("2. Description indicates 'ONLY if absolutely needed'")
print("3. Counter prevents multiple clarifications")
