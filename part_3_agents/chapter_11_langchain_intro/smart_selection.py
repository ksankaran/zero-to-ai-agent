# From: Zero to AI Agent, Chapter 11, Section 11.5
# File: smart_selection.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

class SmartModelSelector:
    def __init__(self):
        # Classifier to determine complexity
        self.classifier = ChatOpenAI(temperature=0)
        
        self.classify_prompt = ChatPromptTemplate.from_template(
            "Is this question simple or complex? Reply with one word.\n"
            "Question: {question}"
        )
        
        # Different models for different complexities
        self.simple_model = ChatOpenAI(model="gpt-3.5-turbo")
        self.complex_model = ChatOpenAI(model="gpt-4")
    
    def answer(self, question):
        """Pick model based on question complexity"""
        # Classify question
        classify_chain = self.classify_prompt | self.classifier
        result = classify_chain.invoke({"question": question})
        complexity = result.content.strip().lower()
        
        # Choose model
        if complexity == "complex":
            print("[Using GPT-4 for complex question]")
            model = self.complex_model
        else:
            print("[Using GPT-3.5 for simple question]")
            model = self.simple_model
        
        # Get answer
        response = model.invoke(question)
        return response.content

# Test it
selector = SmartModelSelector()

print("Simple:", selector.answer("What's the capital of France?"))
print("\nComplex:", selector.answer("Explain the philosophical implications of quantum mechanics"))
