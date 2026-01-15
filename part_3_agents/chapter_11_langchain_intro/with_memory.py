# From: Zero to AI Agent, Chapter 11, Section 11.4
# File: with_memory.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()

# Set up memory
memory = ConversationBufferMemory(return_messages=True)

# Prompt that includes conversation history
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

llm = ChatOpenAI()
chain = prompt | llm

# Have a conversation
def chat(message):
    # Get history
    history = memory.load_memory_variables({})["history"]
    
    # Get response
    response = chain.invoke({
        "history": history,
        "input": message
    })
    
    # Save to memory
    memory.save_context(
        {"input": message},
        {"output": response.content}
    )
    
    return response.content

# Test memory
print(chat("Hi! My name is Alice"))
print(chat("What's my name?"))  # It should remember!
