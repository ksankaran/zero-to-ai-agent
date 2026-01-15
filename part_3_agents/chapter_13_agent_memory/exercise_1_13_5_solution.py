# From: AI Agents Book - Chapter 13, Section 13.5
# File: exercise_1_13_5_solution.py
# Exercise: Basic Semantic Search

from dotenv import load_dotenv
load_dotenv()

import chromadb
from openai import OpenAI


class SemanticMemory:
    """Simple semantic memory using ChromaDB."""
    
    def __init__(self):
        self.openai = OpenAI()
        self.chroma = chromadb.Client()
        self.collection = self.chroma.create_collection("memories")
        self.count = 0
    
    def _embed(self, text):
        """Get embedding vector for text."""
        response = self.openai.embeddings.create(
            model="text-embedding-3-small", input=text
        )
        return response.data[0].embedding
    
    def add(self, text):
        """Add text to memory."""
        self.count += 1
        self.collection.add(
            ids=[f"m{self.count}"],
            embeddings=[self._embed(text)],
            documents=[text]
        )
    
    def search(self, query, n=3):
        """Find top n most similar memories."""
        results = self.collection.query(
            query_embeddings=[self._embed(query)], n_results=n
        )
        return results["documents"][0]


# Test
memory = SemanticMemory()

# Add facts about different topics
memory.add("Python is a popular programming language")
memory.add("The Eiffel Tower is in Paris, France")
memory.add("Machine learning requires lots of data")
memory.add("Pizza originated in Italy")
memory.add("Neural networks mimic brain structure")

# Search for related concepts
print("Query: 'AI and data science'")
for result in memory.search("AI and data science"):
    print(f"  - {result}")

print("\nQuery: 'European landmarks'")
for result in memory.search("European landmarks"):
    print(f"  - {result}")
