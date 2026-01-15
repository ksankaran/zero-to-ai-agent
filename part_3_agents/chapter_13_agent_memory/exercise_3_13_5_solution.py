# From: AI Agents Book - Chapter 13, Section 13.5
# File: exercise_3_13_5_solution.py
# Exercise: Conversational Agent with Semantic Recall

from dotenv import load_dotenv
load_dotenv()

import chromadb
from openai import OpenAI


class SemanticAgent:
    """Agent with semantic memory and debug output."""
    
    def __init__(self, system_prompt):
        self.openai = OpenAI()
        self.system_prompt = system_prompt
        self.history = []
        self.chroma = chromadb.Client()
        self.memories = self.chroma.create_collection("agent_mem")
        self.mem_id = 0
    
    def _embed(self, text):
        """Get embedding for text."""
        return self.openai.embeddings.create(
            model="text-embedding-3-small", input=text
        ).data[0].embedding
    
    def _store(self, content):
        """Store content in semantic memory."""
        self.mem_id += 1
        self.memories.add(
            ids=[f"m{self.mem_id}"],
            embeddings=[self._embed(content)],
            documents=[content]
        )
    
    def _retrieve(self, query, n=3):
        """Retrieve relevant memories."""
        if self.memories.count() == 0:
            return []
        results = self.memories.query(
            query_embeddings=[self._embed(query)],
            n_results=min(n, self.memories.count())
        )
        return results["documents"][0]
    
    def remember(self, fact):
        """Explicitly store a fact."""
        self._store(f"Fact: {fact}")
        return f"Stored: {fact}"
    
    def chat(self, user_input):
        """Process user input with semantic recall."""
        # Retrieve relevant memories
        relevant = self._retrieve(user_input)
        
        # Build messages
        messages = [{"role": "system", "content": self.system_prompt}]
        if relevant:
            mem_str = "\n".join(f"- {m}" for m in relevant)
            messages.append({"role": "system", "content": f"Relevant memories:\n{mem_str}"})
            print(f"[DEBUG] Retrieved: {relevant}")
        
        messages.extend(self.history[-10:])
        messages.append({"role": "user", "content": user_input})
        
        # Get response
        response = self.openai.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = response.choices[0].message.content
        
        # Update history and memory
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": reply})
        self._store(f"Discussed: {user_input[:80]}")
        
        return reply


# Test
agent = SemanticAgent("You are a helpful assistant with a good memory.")

# Store some facts
print(agent.remember("User's favorite color is blue"))
print(agent.remember("User is learning Python programming"))
print(agent.remember("User has a meeting on Friday at 2pm"))

print("\n" + "=" * 50)

# Chat with semantic recall
print("\nUser: I'm working on some code today")
print(f"Agent: {agent.chat('I am working on some code today')}")

print("\nUser: What do you know about my schedule?")
print(f"Agent: {agent.chat('What do you know about my schedule?')}")

print("\nUser: What are my preferences?")
print(f"Agent: {agent.chat('What are my preferences?')}")
