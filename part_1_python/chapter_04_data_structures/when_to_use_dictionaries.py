# From: Zero to AI Agent, Chapter 4, Section 4.6
# when_to_use_dictionaries.py - When to choose dictionaries for your data

# 1. You need to look up values by a meaningful key
phone_book = {
    "Alice": "555-1234",
    "Bob": "555-5678",
    "Charlie": "555-9012"
}
alice_phone = phone_book["Alice"]

# 2. You're mapping relationships
word_counts = {
    "python": 15,
    "code": 8,
    "function": 12
}
python_count = word_counts["python"]

# 3. Storing structured data (like JSON)
user_profile = {
    "username": "alice123",
    "settings": {
        "theme": "dark",
        "notifications": True
    }
}

# 4. Building caches or lookup tables
fibonacci_cache = {
    0: 0,
    1: 1,
    2: 1,
    3: 2,
    4: 3,
    5: 5
}

# 5. Grouping related data
product = {
    "id": "PROD-123",
    "name": "Laptop",
    "price": 999.99,
    "in_stock": True
}

# Real-world DICTIONARY examples in AI:

# API responses (always come as dictionaries/JSON)
ai_response = {
    "text": "Hello! How can I help?",
    "confidence": 0.95,
    "tokens_used": 15,
    "model": "gpt-3.5-turbo"
}

# Feature engineering (mapping features to values)
user_features = {
    "age": 25,
    "purchase_count": 10,
    "is_premium": True,
    "last_activity": "2024-01-15"
}

# Entity tracking in NLP
entities = {
    "persons": ["Alice", "Bob"],
    "locations": ["New York", "Boston"],
    "organizations": ["OpenAI", "Google"]
}

print("Dictionary examples:")
print(f"Alice's phone: {alice_phone}")
print(f"Python word count: {python_count}")
print(f"AI response confidence: {ai_response['confidence']}")
print(f"Entities found: {len(entities)} types")
