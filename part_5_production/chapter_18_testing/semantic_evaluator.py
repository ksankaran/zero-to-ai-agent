# From: AI Agents Book, Chapter 18, Section 18.3
# File: semantic_evaluator.py
# Description: Evaluate responses using semantic similarity with embeddings

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
import numpy as np

load_dotenv()


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


class SemanticEvaluator:
    """Evaluate responses using semantic similarity."""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
    
    def evaluate(self, response: str, reference: str, threshold: float = 0.85) -> dict:
        """Compare response to reference using embeddings."""
        response_embedding = self.embeddings.embed_query(response)
        reference_embedding = self.embeddings.embed_query(reference)
        
        similarity = cosine_similarity(response_embedding, reference_embedding)
        
        return {
            "metric": "semantic_similarity",
            "score": similarity,
            "threshold": threshold,
            "passed": similarity >= threshold
        }


# Example usage
if __name__ == "__main__":
    evaluator = SemanticEvaluator()
    
    # These have different words but same meaning
    response = "Paris is the capital of France."
    reference = "The capital city of France is Paris."
    
    result = evaluator.evaluate(response, reference)
    print(f"Semantic similarity: {result['score']:.3f}")
    print(f"Passed: {result['passed']}")
