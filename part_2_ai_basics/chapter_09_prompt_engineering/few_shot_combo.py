# From: Zero to AI Agent, Chapter 9, Section 9.3
# File: few_shot_combo.py

"""
Combining instructions with examples for powerful prompts
"""

prompt = """You are a technical documentation writer. Convert API responses to user-friendly descriptions.

Rules:
- Remove technical jargon
- Focus on what the user can do
- Keep it under 50 words

Examples:

API: {"status": 200, "user_id": 12345, "permissions": ["read", "write"]}
Description: Your account is set up successfully! You can now view and edit documents.

API: {"error": 403, "message": "Invalid authentication token"}
Description: We couldn't verify your login. Please sign in again to continue.

Now convert:
API: {"status": 201, "resource": "file_uploaded", "size_mb": 2.4}
Description:"""

# This combines:
# - System-level instructions (role, rules)
# - Few-shot examples (showing the pattern)  
# - Clear task (convert this specific input)

if __name__ == "__main__":
    print("FEW-SHOT + INSTRUCTIONS COMBO")
    print("="*50)
    print("This prompt combines:")
    print("1. Role definition")
    print("2. Clear rules")
    print("3. Two examples showing the pattern")
    print("4. The actual task")
    print("\nExpected output: 'Your file uploaded successfully! The 2.4 MB file is ready to use.'")