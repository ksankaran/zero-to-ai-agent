# From: Zero to AI Agent, Chapter 5, Section 5.6
# File: ai_modules_preview.py

# These are the big ones for AI - we'll use them later!

# numpy - Numerical computing
# pip install numpy
import numpy as np
array = np.array([1, 2, 3, 4, 5])
print(f"NumPy array: {array}")
print(f"Mean: {array.mean()}, Std: {array.std()}")

# pandas - Data manipulation
# pip install pandas
import pandas as pd
data = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "score": [95, 87, 92]
})
print("\nPandas DataFrame:")
print(data)

# For AI/ML (we'll cover these in detail later):
# - openai (GPT models)
# - anthropic (Claude API)
# - langchain (AI application framework)
# - transformers (Hugging Face models)
# - tensorflow / pytorch (deep learning)