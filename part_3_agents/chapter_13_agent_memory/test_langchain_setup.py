# From: AI Agents Book - Chapter 13, Section 13.6
# File: test_langchain_setup.py

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-3.5-turbo")
response = llm.invoke([HumanMessage(content="Hello!")])
print(response.content)
print("LangChain is ready!")
