# From: AI Agents Book - Chapter 13, Section 13.5
# File: semantic_memory.py

from dotenv import load_dotenv
load_dotenv()

import chromadb
from openai import OpenAI


class SemanticMemory:
    """Vector-based memory for semantic search."""
    
    def __init__(self, collection_name="memories"):
        self.openai = OpenAI()
        self.chroma = chromadb.Client()
        self.collection = self.chroma.create_collection(name=collection_name)
        self.memory_count = 0
    
    def _get_embedding(self, text):
        """Get embedding vector for text."""
        response = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def add(self, content, metadata=None):
        """Store a memory with its embedding."""
        self.memory_count += 1
        memory_id = f"mem_{self.memory_count}"
        
        self.collection.add(
            ids=[memory_id],
            embeddings=[self._get_embedding(content)],
            documents=[content],
            metadatas=[metadata or {}]
        )
        return memory_id
    
    def search(self, query, n_results=5):
        """Find memories similar to the query."""
        results = self.collection.query(
            query_embeddings=[self._get_embedding(query)],
            n_results=n_results
        )
        
        memories = []
        for i, doc in enumerate(results["documents"][0]):
            memories.append({
                "content": doc,
                "metadata": results["metadatas"][0][i],
                "id": results["ids"][0][i]
            })
        return memories
    
    def count(self):
        """Return total number of memories."""
        return self.collection.count()


# Example usage
if __name__ == "__main__":
    memory = SemanticMemory()
    
    # Add various memories
    memory.add("Sarah is leading the backend team", {"type": "person"})
    memory.add("The project deadline is March 15th", {"type": "project"})
    memory.add("Team velocity has improved by 20%", {"type": "metrics"})
    
    print(f"Total memories: {memory.count()}")
    
    # Search by meaning
    results = memory.search("How is the team performing?")
    print("\nSearch results for 'How is the team performing?':")
    for r in results:
        print(f"  - {r['content']}")
