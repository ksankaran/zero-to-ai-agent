# From: Zero to AI Agent, Chapter 12, Section 12.7
# File: first_agent.py

from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_classic.agents import create_react_agent, AgentExecutor
from langsmith import Client
from dotenv import load_dotenv
import os

load_dotenv()

# Step 1: Create a tool
def multiply(numbers: str) -> str:
    """Multiply two numbers separated by comma."""
    try:
        a, b = map(float, numbers.split(','))
        return str(a * b)
    except:
        return "Error: Please provide two numbers separated by comma"

multiply_tool = Tool(
    name="Multiplier",
    func=multiply,
    description="Multiply two numbers. Input format: 'number1,number2'"
)

# Step 2: Create the LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Step 3: Get the ReAct prompt from LangSmith
# You need LANGSMITH_API_KEY from https://smith.langchain.com/
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
client = Client(api_key=langsmith_api_key)
prompt = client.pull_prompt("hwchase17/react")

# Step 4: Create the agent
agent = create_react_agent(
    llm=llm,
    tools=[multiply_tool],
    prompt=prompt
)

# Step 5: Create the executor (this runs the agent)
agent_executor = AgentExecutor(
    agent=agent,
    tools=[multiply_tool],
    verbose=True,  # See the thinking process!
    max_iterations=3  # Safety limit
)

# Step 6: Use your agent!
result = agent_executor.invoke({
    "input": "What is 15 times 24?"
})

print(f"\nFinal Answer: {result['output']}")
