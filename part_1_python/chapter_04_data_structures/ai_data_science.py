# From: Zero to AI Agent, Chapter 4, Section 4.7
# ai_data_science.py - List comprehensions for AI and data science

# Preparing text data for NLP
raw_texts = ["Hello World!", "  Python AI  ", "Machine Learning"]

# Clean and tokenize
processed = [text.strip().lower().split() for text in raw_texts]
print("Tokenized:", processed)
# [['hello', 'world!'], ['python', 'ai'], ['machine', 'learning']]

# Filter out short words
filtered = [[word for word in text if len(word) > 2] for text in processed]
print("Filtered:", filtered)

# Creating feature vectors
words = ["python", "ai", "machine", "learning"]
vocabulary = ["python", "java", "ai", "machine", "learning", "code"]

# Binary features (1 if word in vocabulary, 0 if not)
features = [1 if word in words else 0 for word in vocabulary]
print("Features:", features)  # [1, 0, 1, 1, 1, 0]

# Batch processing
data = list(range(20))
batch_size = 5

# Create batches
batches = [data[i:i+batch_size] for i in range(0, len(data), batch_size)]
print("Batches:", batches)
# [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]]

# Normalizing scores
scores = [85, 92, 78, 95, 88]
max_score = max(scores)
normalized = [score / max_score for score in scores]
print("Normalized:", normalized)
