# From: AI Agents Book - Chapter 13, Section 13.6
# File: summary_memory_modern.py

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


class SummaryMemory:
    """Custom summary memory implementation for modern LangChain."""
    
    def __init__(self, llm, max_messages=10):
        self.llm = llm
        self.max_messages = max_messages
        self.messages = []
        self.summary = ""
    
    def add_exchange(self, human_msg: str, ai_msg: str):
        """Add a human-AI exchange to memory."""
        self.messages.append(HumanMessage(content=human_msg))
        self.messages.append(AIMessage(content=ai_msg))
        
        if len(self.messages) > self.max_messages:
            self._summarize()
    
    def _summarize(self):
        """Summarize older messages to compress memory."""
        to_summarize = self.messages[:-4]
        to_keep = self.messages[-4:]
        
        summary_prompt = f"""Summarize concisely, preserving key facts:
Previous: {self.summary}
New: {self._format(to_summarize)}
Updated summary:"""
        
        response = self.llm.invoke([HumanMessage(content=summary_prompt)])
        self.summary = response.content
        self.messages = to_keep
    
    def _format(self, messages):
        """Format messages for summary prompt."""
        return "\n".join(
            f"{'H' if isinstance(m, HumanMessage) else 'A'}: {m.content}" 
            for m in messages
        )
    
    def get_context(self):
        """Get messages to include in context."""
        context = []
        if self.summary:
            context.append(SystemMessage(content=f"Earlier: {self.summary}"))
        context.extend(self.messages)
        return context


# Usage example
if __name__ == "__main__":
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    memory = SummaryMemory(llm, max_messages=6)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    chain = prompt | llm
    
    test_messages = [
        "I'm planning a Japan trip.",
        "Budget is $5000.",
        "I love temples.",
        "What should I prioritize?"
    ]
    
    for msg in test_messages:
        messages = memory.get_context() + [HumanMessage(content=msg)]
        response = chain.invoke({"history": messages, "input": msg})
        print(f"H: {msg}\nA: {response.content[:80]}...\n")
        memory.add_exchange(msg, response.content)
