# From: AI Agents Book - Chapter 13, Section 13.5
# File: test_chromadb.py

import chromadb

# Create a client (in-memory by default)
client = chromadb.Client()

# Create a collection (like a table)
collection = client.create_collection("test")

# Add some data
collection.add(
    ids=["id1", "id2"],
    documents=["Hello world", "Goodbye world"]
)

print(f"Collection has {collection.count()} items")
# Output: Collection has 2 items
