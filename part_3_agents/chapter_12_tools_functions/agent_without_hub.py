# From: Zero to AI Agent, Chapter 12, Section 12.7
# File: agent_without_hub.py

from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_classic.agents import AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_classic.agents.format_scratchpad import format_log_to_str
from langchain_classic.agents.output_parsers import ReActSingleInputOutputParser
from dotenv import load_dotenv

load_dotenv()

# Create a tool
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

# Create the ReAct prompt manually (this is what hub.pull does)
template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

# Create LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Bind tools to LLM
llm_with_stop = llm.bind(stop=["\nObservation"])

# Create the agent chain
agent = (
    {
        "input": lambda x: x["input"],
        "tools": lambda x: "\n".join([f"{tool.name}: {tool.description}" for tool in [multiply_tool]]),
        "tool_names": lambda x: ", ".join([tool.name for tool in [multiply_tool]]),
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
    }
    | prompt
    | llm_with_stop
    | ReActSingleInputOutputParser()
)

# Create executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=[multiply_tool],
    verbose=True
)

# Use it!
result = agent_executor.invoke({"input": "What is 15 times 24?"})
print(f"\nFinal Answer: {result['output']}")
