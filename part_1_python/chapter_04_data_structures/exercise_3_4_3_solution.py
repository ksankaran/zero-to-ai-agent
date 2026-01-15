# From: Zero to AI Agent, Chapter 4, Section 4.3
# Exercise 3: Model Configuration Validator

# Define model configs as tuples
configs = [
    ("small_model", 4, 10_000_000, 0.001),
    ("medium_model", 8, 100_000_000, 0.0001),
    ("large_model", 12, 1_000_000_000, 0.00001)
]

# Store configurations
model_registry = {}
for config in configs:
    name, layers, params, lr = config
    model_registry[name] = config
    print(f"Registered: {name} - {layers} layers, {params:,} params, LR: {lr}")

# Validate configs haven't changed (immutability check)
original_config = configs[0]
# Can't modify: original_config[1] = 5  # Would raise TypeError

# Find smallest and largest models
smallest = min(configs, key=lambda c: c[2])
largest = max(configs, key=lambda c: c[2])

print(f"\nSmallest model: {smallest[0]} with {smallest[2]:,} parameters")
print(f"Largest model: {largest[0]} with {largest[2]:,} parameters")

# Unpack and display config details
for name, config in model_registry.items():
    model_name, num_layers, num_params, learning_rate = config
    print(f"\n{model_name}:")
    print(f"  Layers: {num_layers}")
    print(f"  Parameters: {num_params:,}")
    print(f"  Learning Rate: {learning_rate}")
