# From: Zero to AI Agent, Chapter 19, Section 19.1
# File: simple_agent.py

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# Load environment variables
load_dotenv()

class AgentState(TypedDict):
    question: str
    answer: str

def process_question(state: AgentState) -> AgentState:
    """Simple node that answers a question."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = llm.invoke(state["question"])
    return {"answer": response.content}

# Build the graph
graph = StateGraph(AgentState)
graph.add_node("process", process_question)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()

if __name__ == "__main__":
    result = agent.invoke({"question": "What is the capital of France?"})
    print(f"Answer: {result['answer']}")
