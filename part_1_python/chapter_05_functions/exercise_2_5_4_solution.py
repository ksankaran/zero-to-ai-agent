# From: Zero to AI Agent, Chapter 5, Section 5.4
# File: exercise_2_5_4_solution.py

def analyze_text(text):
    """Analyze text and return statistics"""
    # Clean the text
    text = text.strip()
    
    if not text:
        return {
            "word_count": 0,
            "sentence_count": 0,
            "average_word_length": 0
        }
    
    # Count words
    words = text.split()
    word_count = len(words)
    
    # Count sentences (simple approach)
    sentence_count = text.count('.') + text.count('!') + text.count('?')
    if sentence_count == 0:  # No punctuation, count as 1 sentence
        sentence_count = 1
    
    # Calculate average word length
    total_length = sum(len(word.strip('.,!?;:')) for word in words)
    average_word_length = total_length / word_count if word_count > 0 else 0
    
    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "average_word_length": round(average_word_length, 2)
    }

def compare_texts(text1, text2):
    """Compare two texts and return analysis"""
    # Analyze both texts
    stats1 = analyze_text(text1)
    stats2 = analyze_text(text2)
    
    # Determine which is longer
    if stats1["word_count"] > stats2["word_count"]:
        longer = "Text 1"
        difference = stats1["word_count"] - stats2["word_count"]
    elif stats2["word_count"] > stats1["word_count"]:
        longer = "Text 2"
        difference = stats2["word_count"] - stats1["word_count"]
    else:
        longer = "Both texts are equal"
        difference = 0
    
    # Return comprehensive comparison
    return {
        "text1_stats": stats1,
        "text2_stats": stats2,
        "longer_text": longer,
        "word_difference": difference,
        "more_complex": "Text 1" if stats1["average_word_length"] > stats2["average_word_length"] else "Text 2"
    }

def print_comparison(comparison):
    """Print formatted comparison"""
    print("\n" + "="*50)
    print("TEXT COMPARISON RESULTS")
    print("="*50)
    
    print("\nText 1 Statistics:")
    stats1 = comparison["text1_stats"]
    print(f"  Words: {stats1['word_count']}")
    print(f"  Sentences: {stats1['sentence_count']}")
    print(f"  Avg word length: {stats1['average_word_length']} chars")
    
    print("\nText 2 Statistics:")
    stats2 = comparison["text2_stats"]
    print(f"  Words: {stats2['word_count']}")
    print(f"  Sentences: {stats2['sentence_count']}")
    print(f"  Avg word length: {stats2['average_word_length']} chars")
    
    print("\nComparison:")
    print(f"  Longer text: {comparison['longer_text']}")
    if comparison["word_difference"] > 0:
        print(f"  Difference: {comparison['word_difference']} words")
    print(f"  More complex vocabulary: {comparison['more_complex']}")
    print("="*50)

# Test the system
text1 = "Python is amazing. It makes programming fun and accessible!"
text2 = "Artificial intelligence is transforming how we interact with technology. Machine learning enables computers to learn from data."

result = compare_texts(text1, text2)
print_comparison(result)

# Test with the individual function
stats = analyze_text(text1)
print(f"\nQuick analysis of text1: {stats}")