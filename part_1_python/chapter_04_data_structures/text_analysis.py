# From: Zero to AI Agent, Chapter 4, Section 4.7
# text_analysis.py - Real-world text analysis with comprehensions

# Sample text data
documents = [
    "Python is great for AI and machine learning",
    "Data science requires Python skills",
    "Machine learning is part of artificial intelligence",
    "Python makes data analysis easy"
]

# Tokenize all documents (split into words)
tokenized = [doc.lower().split() for doc in documents]
print("Tokenized documents:")
for i, tokens in enumerate(tokenized):
    print(f"  Doc {i}: {tokens[:5]}...")  # Show first 5 words

# Extract all unique words (vocabulary)
all_words = [word for doc in tokenized for word in doc]
vocabulary = list(set(all_words))
print(f"\nVocabulary size: {len(vocabulary)}")

# Count word frequencies
word_freq = {}
for word in all_words:
    if word not in word_freq:
        word_freq[word] = 0
    word_freq[word] += 1

# Find common words (appear more than once)
common_words = [word for word, freq in word_freq.items() if freq > 1]
print(f"Common words: {common_words}")

# Create document vectors (1 if word appears, 0 if not)
target_words = ["python", "ai", "machine", "learning", "data"]

doc_vectors = []
for doc in tokenized:
    vector = [1 if word in doc else 0 for word in target_words]
    doc_vectors.append(vector)

print("\nDocument vectors:")
print("Words:", target_words)
for i, vector in enumerate(doc_vectors):
    print(f"Doc {i}: {vector}")

# Find documents containing "python"
python_docs = [i for i, doc in enumerate(tokenized) if "python" in doc]
print(f"\nDocuments containing 'python': {python_docs}")
