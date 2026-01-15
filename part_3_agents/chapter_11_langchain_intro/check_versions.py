# From: Zero to AI Agent, Chapter 11, Section 11.2
# File: check_versions.py

import langchain

print(f"LangChain version: {langchain.__version__}")

# Save your working setup
import subprocess
subprocess.run(["pip", "freeze", ">", "requirements.txt"], shell=True)
print("Saved package versions to requirements.txt")
