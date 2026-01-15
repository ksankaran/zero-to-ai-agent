# From: AI Agents Book - Chapter 13, Section 13.5
# File: exercise_2_13_5_solution.py
# Exercise: Memory with Categories

from dotenv import load_dotenv
load_dotenv()

import chromadb
from openai import OpenAI


class CategorizedMemory:
    """Semantic memory with category filtering."""
    
    def __init__(self):
        self.openai = OpenAI()
        self.chroma = chromadb.Client()
        self.collection = self.chroma.create_collection("categorized")
        self.count = 0
        self.categories = {}
    
    def _embed(self, text):
        """Get embedding vector for text."""
        response = self.openai.embeddings.create(
            model="text-embedding-3-small", input=text
        )
        return response.data[0].embedding
    
    def add(self, text, category):
        """Add text with a category."""
        self.count += 1
        self.collection.add(
            ids=[f"m{self.count}"],
            embeddings=[self._embed(text)],
            documents=[text],
            metadatas=[{"category": category}]
        )
        self.categories[category] = self.categories.get(category, 0) + 1
    
    def search(self, query, n=3):
        """Search all memories."""
        results = self.collection.query(
            query_embeddings=[self._embed(query)], n_results=n
        )
        return results["documents"][0]
    
    def search_category(self, query, category, n=3):
        """Search within a specific category."""
        results = self.collection.query(
            query_embeddings=[self._embed(query)],
            n_results=n,
            where={"category": category}
        )
        return results["documents"][0] if results["documents"] else []
    
    def get_category_counts(self):
        """Return count of memories per category."""
        return self.categories.copy()


# Test
memory = CategorizedMemory()

# Add memories with categories
memory.add("Finish quarterly report by Friday", "work")
memory.add("Team meeting moved to 3pm", "work")
memory.add("Prepare presentation for client", "work")
memory.add("Buy groceries for dinner party", "personal")
memory.add("Call mom for her birthday", "personal")
memory.add("App idea: habit tracker with AI coaching", "ideas")
memory.add("Blog post concept: future of remote work", "ideas")

print("Category counts:", memory.get_category_counts())

print("\nAll memories - search 'deadlines':")
for r in memory.search("deadlines"):
    print(f"  - {r}")

print("\nWork only - search 'deadlines':")
for r in memory.search_category("deadlines", "work"):
    print(f"  - {r}")

print("\nIdeas only - search 'technology':")
for r in memory.search_category("technology", "ideas"):
    print(f"  - {r}")
