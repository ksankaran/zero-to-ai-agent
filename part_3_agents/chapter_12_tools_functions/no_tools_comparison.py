# From: Zero to AI Agent, Chapter 12, Section 12.1
# File: no_tools_comparison.py

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

# Load your OpenAI API key
load_dotenv()

# Create our LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Without tools - the LLM can only guess
print("WITHOUT TOOLS - The LLM tries its best:")
print("-" * 40)

response = llm.invoke([
    HumanMessage(content="What is 15,847 * 3,921?")
])

print("User: What is 15,847 * 3,921?")
print(f"AI: {response.content}")
print("\n(The AI might attempt the math, but could be wrong!)")

# Try another question that needs real-world data
response2 = llm.invoke([
    HumanMessage(content="What's the current temperature in Tokyo?")
])

print("\nUser: What's the current temperature in Tokyo?")
print(f"AI: {response2.content}")
print("\n(The AI can only guess or use outdated training data!)")
