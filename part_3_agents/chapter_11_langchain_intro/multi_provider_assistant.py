# From: Zero to AI Agent, Chapter 11, Section 11.5
# File: multi_provider_assistant.py

from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv()

class MultiProviderAssistant:
    def __init__(self):
        self.memory = ConversationBufferMemory(return_messages=True)
        
        # Available models
        self.models = {
            "fast": ChatOpenAI(model="gpt-3.5-turbo"),
            "smart": ChatOpenAI(model="gpt-4"),
            "private": Ollama(model="llama2")
        }
        
        self.current_model = "fast"
        
        # Conversation prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
    
    def switch_model(self, model_name):
        """Switch to different model"""
        if model_name in self.models:
            self.current_model = model_name
            return f"Switched to {model_name} model"
        return "Model not available"
    
    def chat(self, message):
        """Chat with current model"""
        # Get history
        history = self.memory.load_memory_variables({})["history"]
        
        # Build chain with current model
        model = self.models[self.current_model]
        chain = self.prompt | model
        
        # Get response
        response = chain.invoke({
            "history": history,
            "input": message
        })
        
        # Extract content
        if hasattr(response, 'content'):
            content = response.content
        else:
            content = str(response)
        
        # Save to memory
        self.memory.save_context(
            {"input": message},
            {"output": content}
        )
        
        return content

# Interactive session
def run():
    assistant = MultiProviderAssistant()
    
    print("Multi-Provider Assistant Ready!")
    print("Commands: 'switch:fast/smart/private', 'quit'\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'quit':
            break
        elif user_input.startswith('switch:'):
            model = user_input.split(':')[1]
            print(assistant.switch_model(model))
        else:
            print(f"Assistant ({assistant.current_model}):", 
                  assistant.chat(user_input))

if __name__ == "__main__":
    run()
