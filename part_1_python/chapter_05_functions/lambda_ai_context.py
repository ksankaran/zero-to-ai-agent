# From: Zero to AI Agent, Chapter 5, Section 5.5
# File: lambda_ai_context.py

# Example: Preprocessing text for AI
texts = [
    "  Hello, World!  ",
    "PYTHON is AWESOME",
    "  ai and ml  "
]

# Clean texts using lambda
cleaned = list(map(lambda text: text.strip().lower(), texts))
print("Cleaned texts:", cleaned)

# Example: Configuring AI responses
responses = [
    {"text": "Hello!", "confidence": 0.95},
    {"text": "Hi there!", "confidence": 0.87},
    {"text": "Greetings!", "confidence": 0.73}
]

# Get best response (highest confidence)
best = max(responses, key=lambda r: r["confidence"])
print(f"Best response: '{best['text']}' (confidence: {best['confidence']})")

# Filter high-confidence responses
high_confidence = list(filter(lambda r: r["confidence"] > 0.8, responses))
print(f"High confidence responses: {len(high_confidence)}")