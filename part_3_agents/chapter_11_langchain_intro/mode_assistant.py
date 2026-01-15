# From: Zero to AI Agent, Chapter 11, Section 11.4
# File: mode_assistant.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

class ModeAssistant:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7)
        self.mode = "normal"
        
        # Different prompts for different modes
        self.prompts = {
            "normal": "Answer this: {input}",
            "creative": "Be very creative and imaginative: {input}",
            "teacher": "Explain this like a patient teacher: {input}",
            "concise": "Answer in one sentence: {input}"
        }
    
    def set_mode(self, mode):
        """Change conversation mode"""
        if mode in self.prompts:
            self.mode = mode
            return f"Mode changed to: {mode}"
        return "Unknown mode"
    
    def respond(self, message):
        """Respond based on current mode"""
        prompt = ChatPromptTemplate.from_template(self.prompts[self.mode])
        chain = prompt | self.llm
        response = chain.invoke({"input": message})
        return response.content

# Test different modes
assistant = ModeAssistant()

question = "What is happiness?"

for mode in ["normal", "creative", "teacher", "concise"]:
    assistant.set_mode(mode)
    print(f"\n{mode.upper()} mode:")
    print(assistant.respond(question)[:150], "...")
