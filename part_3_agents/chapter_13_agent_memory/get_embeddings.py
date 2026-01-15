# From: AI Agents Book - Chapter 13, Section 13.5
# File: get_embeddings.py

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import numpy as np

client = OpenAI()


def get_embedding(text):
    """Convert text to a vector embedding."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def cosine_similarity(v1, v2):
    """Calculate cosine similarity between two vectors."""
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


# Example usage
if __name__ == "__main__":
    # Get embeddings for test sentences
    vec1 = get_embedding("I love programming")
    vec2 = get_embedding("Coding is my passion")
    vec3 = get_embedding("The weather is nice today")
    
    print(f"Vector length: {len(vec1)}")  # 1536 dimensions
    
    # Calculate similarities
    print(f"'programming' vs 'coding': {cosine_similarity(vec1, vec2):.3f}")  # ~0.85
    print(f"'programming' vs 'weather': {cosine_similarity(vec1, vec3):.3f}")  # ~0.45
