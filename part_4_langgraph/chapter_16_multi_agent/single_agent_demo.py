# From: Zero to AI Agent, Chapter 16, Section 16.1
# File: single_agent_demo.py

"""
Demonstrates a single agent handling multiple responsibilities.
"""

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# One big prompt trying to do everything
MEGA_PROMPT = """You are a versatile assistant that can:
1. Analyze text for sentiment, key themes, and statistics
2. Summarize content in different styles
3. Generate creative variations
4. Translate between formats

For any input, determine what the user needs and provide it.
Be analytical when analyzing, creative when creating, 
concise when summarizing."""

text = """
The new product launch exceeded expectations. Sales were up 150% 
compared to our previous launch. Customer feedback has been 
overwhelmingly positive, with 92% satisfaction ratings. However, 
we did face some supply chain challenges that delayed shipments 
to certain regions by 2-3 weeks.
"""

# Single agent tries to do analysis AND summary
response = llm.invoke(f"""
{MEGA_PROMPT}

Please analyze this text AND provide a brief executive summary:

{text}
""")

print("=== Single Agent Response ===")
print(response.content)
