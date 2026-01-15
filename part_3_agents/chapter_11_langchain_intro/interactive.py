# From: Zero to AI Agent, Chapter 11, Section 11.4
# File: interactive.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()

class SimpleAssistant:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7)
        self.memory = ConversationBufferMemory(return_messages=True)
        
        # Create the conversation chain
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful, friendly assistant named Alex."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
    def chat(self, message):
        """Process a message and return response"""
        history = self.memory.load_memory_variables({})["history"]
        
        # Create chain
        chain = self.prompt | self.llm
        
        # Get response
        response = chain.invoke({
            "history": history,
            "input": message
        })
        
        # Update memory
        self.memory.save_context(
            {"input": message},
            {"output": response.content}
        )
        
        return response.content
    
    def reset(self):
        """Start a new conversation"""
        self.memory.clear()
        return "Memory cleared! Starting fresh."

# Interactive loop
def run():
    assistant = SimpleAssistant()
    print("Assistant: Hi! I'm Alex. How can I help? (type 'quit' to exit)")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("Assistant: Goodbye!")
            break
        elif user_input.lower() == 'reset':
            print(f"Assistant: {assistant.reset()}")
        else:
            response = assistant.chat(user_input)
            print(f"Assistant: {response}")

if __name__ == "__main__":
    run()
