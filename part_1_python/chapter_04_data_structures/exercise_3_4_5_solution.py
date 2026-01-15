# From: Zero to AI Agent, Chapter 4, Section 4.5
# Exercise 3: Document Similarity Analyzer

# Sample documents
docs = {
    "doc1": "Python is a great programming language for data science and machine learning",
    "doc2": "Machine learning requires good understanding of Python and statistics",
    "doc3": "Web development with JavaScript and HTML is different from data science",
    "doc4": "Data science involves Python programming and statistical analysis"
}

# Extract unique words (simple tokenization)
doc_words = {}
for doc_id, text in docs.items():
    words = set(text.lower().split())
    # Remove common words
    stop_words = {"is", "a", "for", "and", "with", "of", "from", "the"}
    doc_words[doc_id] = words - stop_words

# Calculate vocabulary overlap
print("Document Vocabulary Overlap:")
for d1 in doc_words:
    for d2 in doc_words:
        if d1 < d2:
            overlap = doc_words[d1] & doc_words[d2]
            print(f"  {d1} & {d2}: {len(overlap)} common words")

# Find common themes
all_words = set.union(*doc_words.values())
word_freq = {}
for word in all_words:
    count = sum(1 for doc in doc_words.values() if word in doc)
    word_freq[word] = count

common_themes = [word for word, count in word_freq.items() if count >= 3]
print(f"\nCommon themes (in 3+ docs): {common_themes}")

# Unique vocabulary
print("\nUnique vocabulary per document:")
for doc_id, words in doc_words.items():
    unique = words.copy()
    for other_id, other_words in doc_words.items():
        if doc_id != other_id:
            unique -= other_words
    if unique:
        print(f"  {doc_id}: {unique}")

# Similarity scores
print("\nSimilarity Scores (Jaccard Index):")
for d1 in doc_words:
    for d2 in doc_words:
        if d1 < d2:
            intersection = len(doc_words[d1] & doc_words[d2])
            union = len(doc_words[d1] | doc_words[d2])
            similarity = intersection / union if union > 0 else 0
            print(f"  {d1}-{d2}: {similarity:.2f}")

# Group similar documents (threshold 0.3)
similar_groups = []
for d1 in doc_words:
    group = {d1}
    for d2 in doc_words:
        if d1 != d2:
            intersection = len(doc_words[d1] & doc_words[d2])
            union = len(doc_words[d1] | doc_words[d2])
            if union > 0 and intersection / union >= 0.3:
                group.add(d2)
    if group not in similar_groups:
        similar_groups.append(group)

print(f"\nSimilar document groups: {similar_groups[:2]}")  # Show first 2 groups
