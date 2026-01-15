# From: Zero to AI Agent, Chapter 4, Section 4.5
# text_processing.py - Using sets for natural language processing

# Text analysis using sets
text1 = "The quick brown fox jumps over the lazy dog and the dog runs away with the fox"
text2 = "Machine learning is a subset of artificial intelligence and artificial intelligence is the future"

# Process text 1
words1 = text1.lower().split()
vocabulary1 = set(words1)  # Unique words

# Process text 2
words2 = text2.lower().split()
vocabulary2 = set(words2)

# Common English stop words
stop_words = {"the", "is", "at", "which", "on", "a", "an", "and", "or", "but", "in", "with", "to", "for", "of"}

# Content words (excluding stop words)
content_words1 = vocabulary1 - stop_words
content_words2 = vocabulary2 - stop_words

# Analysis
print("Text 1 Analysis:")
print(f"  Total words: {len(words1)}")
print(f"  Unique words: {len(vocabulary1)}")
print(f"  Content words: {content_words1}")
print(f"  Lexical diversity: {len(vocabulary1) / len(words1):.2f}")

print("\nText 2 Analysis:")
print(f"  Total words: {len(words2)}")
print(f"  Unique words: {len(vocabulary2)}")
print(f"  Content words: {content_words2}")
print(f"  Lexical diversity: {len(vocabulary2) / len(words2):.2f}")

# Compare vocabularies
print(f"\nCommon content words: {content_words1 & content_words2}")
print(f"Words only in text 1: {content_words1 - content_words2}")
print(f"Words only in text 2: {content_words2 - content_words1}")
