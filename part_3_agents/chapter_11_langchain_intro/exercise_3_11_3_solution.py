# From: Zero to AI Agent, Chapter 11, Section 11.3
# File: exercise_3_11_3_solution.py

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from difflib import SequenceMatcher

load_dotenv()

def compare_temperatures(prompt, temp1=0.0, temp2=1.0):
    """Compare outputs at different temperatures"""
    
    # Create models with different temperatures
    focused_model = ChatOpenAI(temperature=temp1)
    creative_model = ChatOpenAI(temperature=temp2)
    
    # Get responses
    focused_response = focused_model.invoke(prompt)
    creative_response = creative_model.invoke(prompt)
    
    focused_text = focused_response.content
    creative_text = creative_response.content
    
    # Count words
    focused_words = focused_text.split()
    creative_words = creative_text.split()
    
    # Calculate similarity
    similarity = SequenceMatcher(None, focused_text, creative_text).ratio()
    
    # Find different words
    focused_set = set(focused_words)
    creative_set = set(creative_words)
    
    unique_to_focused = focused_set - creative_set
    unique_to_creative = creative_set - focused_set
    
    return {
        "focused": focused_text,
        "creative": creative_text,
        "focused_word_count": len(focused_words),
        "creative_word_count": len(creative_words),
        "similarity": similarity,
        "unique_to_focused": unique_to_focused,
        "unique_to_creative": unique_to_creative
    }

# Test prompts
test_prompts = [
    "Write a one-sentence description of coffee",
    "What is the meaning of life?",
    "Describe a sunset"
]

for prompt in test_prompts:
    print(f"📝 Prompt: {prompt}")
    print("=" * 60)
    
    result = compare_temperatures(prompt)
    
    print(f"\n🎯 Temperature 0.0 (Focused):")
    print(result["focused"])
    print(f"Words: {result['focused_word_count']}")
    
    print(f"\n🎨 Temperature 1.0 (Creative):")
    print(result["creative"])
    print(f"Words: {result['creative_word_count']}")
    
    print(f"\n📊 Analysis:")
    print(f"Similarity: {result['similarity']:.1%}")
    print(f"Unique to focused: {len(result['unique_to_focused'])} words")
    print(f"Unique to creative: {len(result['unique_to_creative'])} words")
    
    if result['unique_to_creative']:
        print(f"Creative additions: {list(result['unique_to_creative'])[:5]}")
    
    print("\n" + "="*60 + "\n")

print("💡 Insight: Higher temperature = more variation and creativity!")
