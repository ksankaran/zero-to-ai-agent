# From: Zero to AI Agent, Chapter 11, Section 11.5
# File: gemini_setup.py

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables from .env file
# Add GOOGLE_API_KEY=your-key-here to your .env file
# Get a free API key from makersuite.google.com
load_dotenv()

# Create Gemini model
gemini = ChatGoogleGenerativeAI(model="gemini-pro")

# Use it exactly like OpenAI!
response = gemini.invoke("Hello, Gemini!")
print("Gemini says:", response.content)
