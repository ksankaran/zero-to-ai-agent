# From: Zero to AI Agent, Chapter 20, Section 20.3
# File: scripts/tune_retrieval.py

"""
Tools for tuning retrieval quality.

Note: Make sure you've run 'pip install -e .' from the project root first!
"""

from caspar.knowledge import KnowledgeRetriever


def analyze_retrieval_quality():
    """Analyze retrieval quality with test cases."""
    
    retriever = KnowledgeRetriever()
    retriever.initialize()
    
    # Test cases: (query, expected_source, expected_category)
    test_cases = [
        ("return policy", "policies.md", "policy"),
        ("track my order", "faq.md", "faq"),
        ("laptop won't turn on", "troubleshooting.md", "troubleshooting"),
        ("TechFlow Pro 15 specs", "products.md", "product"),
    ]
    
    print("📊 Retrieval Quality Analysis")
    print("=" * 60)
    
    correct = 0
    total = len(test_cases)
    
    for query, expected_source, expected_category in test_cases:
        results = retriever.retrieve_with_scores(query, k=1)
        
        if results:
            doc, score = results[0]
            actual_source = doc.metadata.get("source", "")
            actual_category = doc.metadata.get("category", "")
            
            source_match = actual_source == expected_source
            category_match = actual_category == expected_category
            
            if source_match and category_match:
                correct += 1
                status = "✅"
            else:
                status = "❌"
            
            print(f"\n{status} Query: '{query}'")
            print(f"   Expected: {expected_source} ({expected_category})")
            print(f"   Got: {actual_source} ({actual_category}) [score: {score:.3f}]")
    
    accuracy = correct / total * 100
    print(f"\n📈 Accuracy: {correct}/{total} ({accuracy:.0f}%)")
    
    if accuracy < 80:
        print("\n💡 Tips to improve:")
        print("   • Add more specific content to knowledge base")
        print("   • Adjust chunk size (try 300-800)")
        print("   • Add section headers for better context")
        print("   • Consider adding synonyms to content")


if __name__ == "__main__":
    analyze_retrieval_quality()
