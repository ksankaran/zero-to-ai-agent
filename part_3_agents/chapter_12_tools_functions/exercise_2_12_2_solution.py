# From: Zero to AI Agent, Chapter 12, Section 12.2
# File: exercise_2_12_2_solution.py

from langchain_core.tools import Tool
import re

def text_stats(text: str) -> str:
    """Calculate text statistics."""
    if not text:
        return "Error: No text provided"
    
    words = text.split()
    word_count = len(words)
    sentences = re.findall(r'[.!?]+', text)
    sentence_count = len(sentences) if sentences else 1
    avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
    
    return f"Words: {word_count}, Sentences: {sentence_count}, Avg word length: {avg_word_length:.1f}"

def extract_keywords(text: str) -> str:
    """Extract top 5 meaningful words."""
    if not text:
        return "Error: No text provided"
    
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'was', 'are'}
    words = text.lower().split()
    meaningful = [w for w in words if w not in stop_words and len(w) > 2]
    
    word_freq = {}
    for word in meaningful:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
    return f"Keywords: {', '.join([w[0] for w in top_words])}"

def summarize(text: str) -> str:
    """Create one-sentence summary."""
    if not text:
        return "Error: No text provided"
    if len(text) < 50:
        return "Text too short to summarize"
    
    sentences = re.split(r'[.!?]+', text)
    first_sentence = sentences[0].strip() if sentences else text[:100]
    return f"Summary: {first_sentence}."

# Create tools
stats_tool = Tool(name="TextStats", func=text_stats, 
                  description="Calculate text statistics")
keywords_tool = Tool(name="ExtractKeywords", func=extract_keywords,
                     description="Extract top keywords from text")
summarize_tool = Tool(name="Summarize", func=summarize,
                      description="Create one-sentence summary")

# Test
if __name__ == "__main__":
    sample_text = "Python is a powerful programming language. It is widely used in data science."
    print(stats_tool.func(sample_text))
    print(keywords_tool.func(sample_text))
    print(summarize_tool.func(sample_text))
