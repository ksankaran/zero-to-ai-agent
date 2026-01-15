# From: Zero to AI Agent, Chapter 11, Section 11.3
# File: prompt_problem.py

# The OLD way - messy and error-prone

name = "Alice"
topic = "Python"

# String concatenation nightmare
prompt = "Hello " + name + ", let me teach you about " + topic

# Or slightly better but still messy
prompt = f"Hello {name}, let me teach you about {topic}"

print(prompt)
