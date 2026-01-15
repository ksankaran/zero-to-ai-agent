# From: Zero to AI Agent, Chapter 11, Section 11.7
# File: debug_wrapper.py

import time
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

class DebugChain:
    """Wrap any chain with debugging"""
    
    def __init__(self, chain, name="Chain"):
        self.chain = chain
        self.name = name
        self.history = []
    
    def invoke(self, inputs):
        """Run with debugging info"""
        
        # Record start
        start = time.time()
        print(f"\n🔍 [{self.name}] Starting...")
        print(f"📥 Inputs: {json.dumps(inputs, indent=2)}")
        
        try:
            # Run the chain
            result = self.chain.invoke(inputs)
            
            # Record success
            elapsed = time.time() - start
            print(f"✅ [{self.name}] Success ({elapsed:.2f}s)")
            
            # Save to history
            self.history.append({
                "inputs": inputs,
                "output": str(result)[:100],  # Truncate
                "time": elapsed,
                "success": True
            })
            
            return result
            
        except Exception as e:
            # Record failure
            print(f"❌ [{self.name}] Failed: {e}")
            
            self.history.append({
                "inputs": inputs,
                "error": str(e),
                "success": False
            })
            
            raise
    
    def show_stats(self):
        """Show debugging statistics"""
        total = len(self.history)
        successes = sum(1 for h in self.history if h["success"])
        
        print(f"\n📊 {self.name} Statistics:")
        print(f"  Total runs: {total}")
        print(f"  Successes: {successes}")
        print(f"  Failures: {total - successes}")
        
        if successes > 0:
            avg_time = sum(h["time"] for h in self.history if h["success"]) / successes
            print(f"  Average time: {avg_time:.2f}s")

# Use it
load_dotenv()

# Create a normal chain
prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
llm = ChatOpenAI()
chain = prompt | llm

# Wrap it for debugging
debug_chain = DebugChain(chain, "TopicExplainer")

# Use it normally
debug_chain.invoke({"topic": "Python"})
debug_chain.invoke({"topic": "LangChain"})

# See statistics
debug_chain.show_stats()
