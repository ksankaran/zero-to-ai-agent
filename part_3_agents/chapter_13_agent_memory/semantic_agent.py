# From: AI Agents Book - Chapter 13, Section 13.5
# File: semantic_agent.py

from dotenv import load_dotenv
load_dotenv()

import chromadb
from openai import OpenAI
from datetime import datetime


class SemanticMemoryAgent:
    """Agent that uses semantic memory for context retrieval."""
    
    def __init__(self, system_prompt):
        self.openai = OpenAI()
        self.system_prompt = system_prompt
        self.conversation = []
        
        # Set up semantic memory
        self.chroma = chromadb.Client()
        self.memories = self.chroma.create_collection("agent_memories")
        self.memory_id = 0
    
    def _embed(self, text):
        """Get embedding for text."""
        response = self.openai.embeddings.create(
            model="text-embedding-3-small", input=text
        )
        return response.data[0].embedding
    
    def _store_memory(self, content, memory_type="conversation"):
        """Store a piece of information in semantic memory."""
        self.memory_id += 1
        self.memories.add(
            ids=[f"m{self.memory_id}"],
            embeddings=[self._embed(content)],
            documents=[content],
            metadatas=[{"type": memory_type, "timestamp": datetime.now().isoformat()}]
        )
    
    def _retrieve_relevant(self, query, n=3):
        """Retrieve memories relevant to the query."""
        if self.memories.count() == 0:
            return []
        
        results = self.memories.query(
            query_embeddings=[self._embed(query)],
            n_results=min(n, self.memories.count())
        )
        return results["documents"][0] if results["documents"] else []
    
    def chat(self, user_input):
        """Process user input and return response."""
        # 1. Retrieve relevant memories
        relevant = self._retrieve_relevant(user_input)
        
        # 2. Build context
        messages = [{"role": "system", "content": self.system_prompt}]
        
        if relevant:
            memory_context = "Relevant information from memory:\n" + "\n".join(f"- {m}" for m in relevant)
            messages.append({"role": "system", "content": memory_context})
        
        messages.extend(self.conversation[-10:])  # Recent conversation
        messages.append({"role": "user", "content": user_input})
        
        # 3. Generate response
        response = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response.choices[0].message.content
        
        # 4. Update conversation history
        self.conversation.append({"role": "user", "content": user_input})
        self.conversation.append({"role": "assistant", "content": reply})
        
        # 5. Store this exchange in semantic memory
        self._store_memory(f"User said: {user_input}")
        self._store_memory(f"Assistant replied about: {user_input[:50]}")
        
        return reply
    
    def remember(self, fact):
        """Explicitly store a fact in memory."""
        self._store_memory(fact, memory_type="explicit")
        return f"I'll remember: {fact}"


# Example usage
if __name__ == "__main__":
    agent = SemanticMemoryAgent(
        system_prompt="You are a helpful project management assistant."
    )
    
    # Have a conversation
    print("Agent: ", agent.chat("Our project is called Phoenix and it's due March 15th"))
    print("Agent: ", agent.chat("Sarah is the tech lead and Tom handles backend"))
    print("Agent: ", agent.chat("We're worried about the authentication module"))
    
    # Later, ask something related
    print("\nAgent: ", agent.chat("What are the main concerns with our project?"))
