# From: AI Agents Book - Chapter 13, Section 13.6
# File: exercise_3_13_6_solution.py
# Exercise: Agent with Tools and Memory Management

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool


# Define tools
@tool
def calculator(expression: str) -> str:
    """Evaluate math expressions like '2+2' or '10*5'."""
    try:
        return f"Result: {eval(expression)}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    weather_db = {
        "Seattle": "Rainy, 55°F",
        "Austin": "Sunny, 85°F",
        "NYC": "Cloudy, 68°F"
    }
    return weather_db.get(city, f"Weather in {city}: Partly cloudy, 70°F")


tools = [calculator, get_weather]


class AgentWithManagedMemory:
    """Agent that manages conversation memory with summarization."""
    
    def __init__(self, max_messages=6, keep_recent=2):
        self.model = ChatOpenAI(model="gpt-4o")
        self.summary_model = ChatOpenAI(model="gpt-3.5-turbo")
        self.max_messages = max_messages
        self.keep_recent = keep_recent
        self.messages = []
        self.summary = ""
        
        # Set up agent
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant with tools. {memory_context}"),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        self.agent = create_react_agent(self.model, tools, self.prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=tools, verbose=False)
    
    def _maybe_summarize(self):
        """Summarize if messages exceed limit."""
        if len(self.messages) <= self.max_messages:
            return
        
        to_summarize = self.messages[:-self.keep_recent]
        to_keep = self.messages[-self.keep_recent:]
        
        summary_text = "\n".join(
            f"{'User' if isinstance(m, HumanMessage) else 'AI'}: {m.content[:100]}"
            for m in to_summarize
        )
        
        prompt = f"Summarize this conversation briefly:\nPrevious summary: {self.summary}\n{summary_text}"
        response = self.summary_model.invoke([HumanMessage(content=prompt)])
        self.summary = response.content
        self.messages = to_keep
        print(f"[Summarized {len(to_summarize)} messages]")
    
    def chat(self, user_input):
        """Chat with memory management."""
        memory_context = f"Previous context: {self.summary}" if self.summary else ""
        
        response = self.executor.invoke({
            "input": user_input,
            "chat_history": self.messages,
            "memory_context": memory_context
        })
        
        self.messages.append(HumanMessage(content=user_input))
        self.messages.append(AIMessage(content=response["output"]))
        
        self._maybe_summarize()
        
        return response["output"]


# Test
if __name__ == "__main__":
    print("=== Agent with Memory Management ===\n")
    
    agent = AgentWithManagedMemory(max_messages=6, keep_recent=2)
    
    # Test with tool calls
    print("1.", agent.chat("What's the weather in Seattle?"))
    print()
    
    print("2.", agent.chat("Calculate 15 * 8"))
    print()
    
    print("3.", agent.chat("What city did I ask about?"))
    print()
    
    # Add more messages to trigger summarization
    for i in range(3):
        print(f"{i+4}.", agent.chat(f"Tell me fact {i+1} about programming.")[:60] + "...")
        print()
    
    # Verify memory works
    print("Memory test:", agent.chat("What calculation did I ask you to do earlier?"))
    print(f"\nTotal messages in memory: {len(agent.messages)}")
    print(f"Summary exists: {bool(agent.summary)}")
