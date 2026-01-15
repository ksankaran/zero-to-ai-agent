# From: Zero to AI Agent, Chapter 4, Section 4.3
# named_tuples.py - Named tuples for clearer code

from collections import namedtuple

# Create a named tuple class for AI model info
ModelInfo = namedtuple('ModelInfo', ['name', 'parameters', 'accuracy', 'trained_on'])

# Create instances
gpt3 = ModelInfo("GPT-3", 175_000_000_000, 0.92, "CommonCrawl")
bert = ModelInfo("BERT", 340_000_000, 0.89, "Wikipedia")

# Access by name (much clearer than index!)
print(f"{gpt3.name} has {gpt3.parameters:,} parameters")
print(f"Accuracy: {gpt3.accuracy}")

# You can still use indexing
print(f"First field: {gpt3[0]}")

# Named tuples are still immutable
# gpt3.accuracy = 0.95  # This would cause an error!

# Create another named tuple for evaluation results
Result = namedtuple('Result', ['model', 'precision', 'recall', 'f1_score'])

# Simulated evaluation
eval_result = Result("MyAgent", 0.89, 0.91, 0.90)
print(f"\nEvaluation Results:")
print(f"Model: {eval_result.model}")
print(f"Precision: {eval_result.precision}")
print(f"Recall: {eval_result.recall}")
print(f"F1 Score: {eval_result.f1_score}")
