# From: Zero to AI Agent, Chapter 12, Section 12.1
# File: first_tool_agent.py

from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun
from langsmith import Client
from dotenv import load_dotenv
import os

load_dotenv()

# Create our LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Use a pre-built tool (we'll learn to make our own in 12.2!)
search = DuckDuckGoSearchRun()

# Create an agent with the search tool
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
client = Client(api_key=langsmith_api_key)
prompt = client.pull_prompt("hwchase17/react")
agent = create_react_agent(llm, [search], prompt)
executor = AgentExecutor(
    agent=agent, 
    tools=[search], 
    verbose=True,  # Show the thinking process!
    max_iterations=3
)

# Ask something that needs current information
print("AGENT WITH SEARCH CAPABILITY")
print("=" * 50)

result = executor.invoke({
    "input": "What is Python programming language known for?"
})

print(f"\nFinal Answer: {result['output']}")