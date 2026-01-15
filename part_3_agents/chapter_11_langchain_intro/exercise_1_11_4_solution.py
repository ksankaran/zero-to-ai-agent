# From: Zero to AI Agent, Chapter 11, Section 11.4
# File: exercise_1_11_4_solution.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.memory import ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()

class SpecializedAssistant:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7)
        self.memory = ConversationBufferMemory(return_messages=True)
        self.current_mode = "translator"
        self.current_style = "formal"
        
        # Translator prompts
        self.translator_prompts = {
            "formal": ChatPromptTemplate.from_template(
                "Rewrite this text in formal, professional language: {text}"
            ),
            "casual": ChatPromptTemplate.from_template(
                "Rewrite this text in casual, friendly language: {text}"
            ),
            "technical": ChatPromptTemplate.from_template(
                "Rewrite this text using technical terminology: {text}"
            )
        }
        
        # Summarizer prompts
        self.summarizer_prompts = {
            "brief": ChatPromptTemplate.from_template(
                "Summarize this in one sentence: {text}"
            ),
            "standard": ChatPromptTemplate.from_template(
                "Summarize this in 3-5 sentences: {text}"
            ),
            "detailed": ChatPromptTemplate.from_template(
                "Provide a detailed summary with key points: {text}"
            )
        }
        
        # Analyzer prompts
        self.analyzer_prompts = {
            "sentiment": ChatPromptTemplate.from_template(
                "Analyze the sentiment and tone of this text: {text}"
            ),
            "structure": ChatPromptTemplate.from_template(
                "Analyze the structure and organization of this text: {text}"
            ),
            "audience": ChatPromptTemplate.from_template(
                "Analyze the target audience for this text: {text}"
            )
        }
    
    def set_mode(self, mode, style="formal"):
        """Switch between translator, summarizer, or analyzer"""
        valid_modes = ["translator", "summarizer", "analyzer"]
        if mode in valid_modes:
            self.current_mode = mode
            self.current_style = style
            return f"Switched to {mode} mode ({style})"
        return "Invalid mode. Choose: translator, summarizer, or analyzer"
    
    def process(self, text):
        """Process text based on current mode and style"""
        
        # Select appropriate prompts
        if self.current_mode == "translator":
            prompts = self.translator_prompts
        elif self.current_mode == "summarizer":
            prompts = self.summarizer_prompts
        else:  # analyzer
            prompts = self.analyzer_prompts
        
        # Get the right prompt for current style
        prompt = prompts.get(self.current_style, prompts[list(prompts.keys())[0]])
        
        # Create chain and process
        chain = prompt | self.llm
        response = chain.invoke({"text": text})
        
        # Save to memory for context
        self.memory.save_context(
            {"input": f"[{self.current_mode}:{self.current_style}] {text}"},
            {"output": response.content}
        )
        
        return response.content

# Test the assistant
assistant = SpecializedAssistant()

test_text = """
Machine learning is a subset of artificial intelligence that enables 
systems to learn and improve from experience without being explicitly programmed.
"""

print("Original text:", test_text)
print("\n" + "="*60 + "\n")

# Test translator mode
for style in ["formal", "casual", "technical"]:
    assistant.set_mode("translator", style)
    result = assistant.process(test_text)
    print(f"TRANSLATOR ({style}):")
    print(result)
    print()

print("="*60 + "\n")

# Test summarizer mode
for style in ["brief", "standard", "detailed"]:
    assistant.set_mode("summarizer", style)
    result = assistant.process(test_text)
    print(f"SUMMARIZER ({style}):")
    print(result)
    print()

print("="*60 + "\n")

# Test analyzer mode
for style in ["sentiment", "structure", "audience"]:
    assistant.set_mode("analyzer", style)
    result = assistant.process(test_text)
    print(f"ANALYZER ({style}):")
    print(result)
    print()
