# From: Zero to AI Agent, Chapter 4, Section 4.4
# dict_patterns.py - Essential dictionary patterns for AI development

# Pattern 1: Configuration Management
agent_config = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_history": 10,
    "system_prompt": "You are a helpful assistant.",
    "features": {
        "memory": True,
        "web_search": False,
        "code_execution": False
    }
}

print("Agent Configuration:")
print(f"  Model: {agent_config['model']}")
print(f"  Temperature: {agent_config['temperature']}")

# Update configuration
agent_config["temperature"] = 0.9
agent_config["max_history"] = 20
print(f"\nUpdated config:")
print(f"  Temperature: {agent_config['temperature']}")
print(f"  Max history: {agent_config['max_history']}")

# Check if feature is enabled
feature_to_check = "memory"
if feature_to_check in agent_config["features"]:
    is_enabled = agent_config["features"][feature_to_check]
    print(f"  {feature_to_check} enabled: {is_enabled}")

# Pattern 2: Response Cache
response_cache = {}

# Create cache key (using tuple as key!)
prompt1 = "What is Python?"
model1 = "gpt-3.5"
cache_key1 = (prompt1.lower().strip(), model1)

# Store response in cache
response_cache[cache_key1] = {
    "response": "Python is a programming language...",
    "timestamp": "2024-01-15 10:30:00",
    "hits": 0
}

# Check cache
prompt2 = "what is python?"  # Different case
model2 = "gpt-3.5"
cache_key2 = (prompt2.lower().strip(), model2)

if cache_key2 in response_cache:
    cached_data = response_cache[cache_key2]
    cached_data["hits"] += 1
    print(f"\nCache hit! Response: {cached_data['response'][:30]}...")
    print(f"Cache hits: {cached_data['hits']}")

# Pattern 3: Entity Tracking
entities = {}

# Track entities mentioned in conversation
entity_mentions = [
    ("Alice", "person", {"age": 30, "role": "developer"}),
    ("Python", "technology", {"version": "3.11"}),
    ("Alice", "person", {"city": "New York"}),  # Update Alice
    ("Bob", "person", {"age": 25})
]

for name, entity_type, attributes in entity_mentions:
    if name not in entities:
        entities[name] = {
            "type": entity_type,
            "mentions": 0,
            "attributes": {}
        }
    
    entities[name]["mentions"] += 1
    entities[name]["attributes"].update(attributes)

print("\nEntity Tracking:")
for name, data in entities.items():
    print(f"  {name} ({data['type']}): {data['mentions']} mentions")
    print(f"    Attributes: {data['attributes']}")
