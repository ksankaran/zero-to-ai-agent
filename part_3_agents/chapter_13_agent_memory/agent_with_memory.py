# From: AI Agents Book - Chapter 13, Section 13.6
# File: agent_with_memory.py
# Note: This uses modern LangChain patterns. Check langchain docs for latest API.

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool

# Define tools
@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression like '2+2' or '10*5'."""
    try:
        return f"Result: {eval(expression)}"
    except:
        return "Error evaluating expression"


@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    weather_data = {"Seattle": "Rainy, 55°F", "NYC": "Sunny, 68°F"}
    return weather_data.get(city, f"Weather in {city}: Partly cloudy, 70°F")


tools = [calculator, get_weather]

# Initialize model
model = ChatOpenAI(model="gpt-4o")

# ReAct prompt template - must include {tools}, {tool_names}, and {agent_scratchpad}
REACT_PROMPT = """You are a helpful assistant with access to tools.

You have access to the following tools:
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

Previous conversation:
{chat_history}

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate.from_template(REACT_PROMPT)

# Create agent
agent = create_react_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Simple conversation with manual history management
chat_history = []


def format_chat_history(history):
    """Format chat history as a string for the prompt."""
    if not history:
        return "No previous conversation."
    
    formatted = []
    for msg in history:
        if isinstance(msg, HumanMessage):
            formatted.append(f"Human: {msg.content}")
        elif isinstance(msg, AIMessage):
            formatted.append(f"Assistant: {msg.content}")
        elif isinstance(msg, str):
            formatted.append(f"Assistant: {msg}")
    return "\n".join(formatted)


def chat(user_input):
    """Chat with the agent, maintaining history."""
    response = agent_executor.invoke({
        "input": user_input,
        "chat_history": format_chat_history(chat_history)
    })
    
    # Update history
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response["output"]))
    
    return response["output"]


if __name__ == "__main__":
    # First interaction
    print("Agent:", chat("What's the weather in Seattle?"))
    
    # Follow-up - agent should remember
    print("Agent:", chat("What city did I just ask about?"))
    
    # Use a tool
    print("Agent:", chat("Calculate 25 * 4"))