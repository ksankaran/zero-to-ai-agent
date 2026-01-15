# From: Zero to AI Agent, Chapter 11, Section 11.7
# File: chain_debugger.py (formerly agent_debugger.py)
# Updated to focus on chain debugging instead of deprecated agent features

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.globals import set_debug, set_verbose
from dotenv import load_dotenv
import time

load_dotenv()

# Example 1: Debug a simple chain
def debug_simple_chain():
    """Debug a basic prompt -> LLM -> parser chain"""
    print("\n=== Debugging Simple Chain ===")
    
    # Turn on verbose mode to see what's happening
    set_verbose(True)
    
    # Create chain components
    prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant. Answer this question: {question}"
    )
    llm = ChatOpenAI(temperature=0)
    parser = StrOutputParser()
    
    # Create the chain
    chain = prompt | llm | parser
    
    # Test with debugging enabled
    print("Testing chain with debugging enabled...")
    try:
        result = chain.invoke({
            "question": "What is the capital of France?"
        })
        print(f"\nFinal answer: {result}")
    except Exception as e:
        print(f"Chain failed: {e}")
        print("\nCommon fixes:")
        print("1. Check prompt variables match input")
        print("2. Verify API key is set")
        print("3. Check model name is valid")
    
    # Turn off verbose mode
    set_verbose(False)

# Example 2: Debug a multi-step chain
def debug_multi_step_chain():
    """Debug a chain with multiple steps"""
    print("\n=== Debugging Multi-Step Chain ===")
    
    # Enable full debug mode for detailed output
    set_debug(True)
    
    # Step 1: Generate a story
    story_prompt = ChatPromptTemplate.from_template(
        "Write a one-sentence story about {animal}"
    )
    
    # Step 2: Extract the moral
    moral_prompt = ChatPromptTemplate.from_template(
        "What is the moral of this story: {story}"
    )
    
    llm = ChatOpenAI(temperature=0.7)
    parser = StrOutputParser()
    
    # Build chains
    story_chain = story_prompt | llm | parser
    
    try:
        # Run first chain
        print("Step 1: Generating story...")
        story = story_chain.invoke({"animal": "a wise owl"})
        print(f"Story: {story}")
        
        # Run second chain with output from first
        print("\nStep 2: Extracting moral...")
        moral_chain = moral_prompt | llm | parser
        moral = moral_chain.invoke({"story": story})
        print(f"Moral: {moral}")
        
    except Exception as e:
        print(f"Multi-step chain failed: {e}")
        print("Debug tip: Check intermediate outputs between steps")
    
    # Turn off debug mode
    set_debug(False)

# Example 3: Debug chain with error handling
def debug_chain_with_errors():
    """Debug common chain errors"""
    print("\n=== Debugging Chain Errors ===")
    
    # Test 1: Missing variable error
    print("\n1. Testing missing variable error:")
    try:
        prompt = ChatPromptTemplate.from_template(
            "Tell me about {topic} and {subtopic}"
        )
        llm = ChatOpenAI()
        chain = prompt | llm
        
        # This will fail - missing 'subtopic'
        result = chain.invoke({"topic": "Python"})
    except KeyError as e:
        print(f"✓ Caught expected error: Missing variable {e}")
        print("Fix: Ensure all template variables are provided")
    
    # Test 2: Invalid model name
    print("\n2. Testing invalid model error:")
    try:
        llm = ChatOpenAI(model="invalid-model-xyz")
        result = llm.invoke("Test")
    except Exception as e:
        print(f"✓ Caught expected error: {str(e)[:50]}...")
        print("Fix: Use valid model names like 'gpt-3.5-turbo' or 'gpt-4'")
    
    # Test 3: Chain with recovery
    print("\n3. Testing chain with fallback:")
    try:
        primary_llm = ChatOpenAI(model="gpt-4", temperature=0)
        fallback_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        
        prompt = ChatPromptTemplate.from_template("Answer: {question}")
        
        # Try primary chain first
        try:
            chain = prompt | primary_llm
            result = chain.invoke({"question": "What is 2+2?"})
            print(f"Primary chain succeeded: {result.content}")
        except:
            # Fallback to simpler model
            print("Primary failed, using fallback...")
            chain = prompt | fallback_llm
            result = chain.invoke({"question": "What is 2+2?"})
            print(f"Fallback chain succeeded: {result.content}")
            
    except Exception as e:
        print(f"Both chains failed: {e}")

# Example 4: Performance debugging
def debug_chain_performance():
    """Debug chain performance"""
    print("\n=== Debugging Chain Performance ===")
    
    prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
    llm = ChatOpenAI()
    parser = StrOutputParser()
    
    # Time each component
    print("Timing chain components:")
    
    # Time prompt formatting
    start = time.time()
    formatted = prompt.format_messages(topic="testing")
    prompt_time = time.time() - start
    print(f"  Prompt formatting: {prompt_time:.4f}s")
    
    # Time LLM call
    start = time.time()
    response = llm.invoke("Quick test")
    llm_time = time.time() - start
    print(f"  LLM call: {llm_time:.2f}s")
    
    # Time full chain
    start = time.time()
    chain = prompt | llm | parser
    result = chain.invoke({"topic": "speed"})
    chain_time = time.time() - start
    print(f"  Full chain: {chain_time:.2f}s")
    
    print(f"\nBottleneck analysis:")
    if llm_time > chain_time * 0.9:
        print("  → LLM call is the bottleneck (normal)")
    if prompt_time > 0.01:
        print("  → Prompt formatting is slow (unusual)")

# Main execution
if __name__ == "__main__":
    print("🔍 LangChain Chain Debugging Examples")
    print("=" * 50)
    
    # Run all debugging examples
    debug_simple_chain()
    debug_multi_step_chain()
    debug_chain_with_errors()
    debug_chain_performance()
    
    print("\n" + "=" * 50)
    print("✅ Debugging examples complete!")
    print("\nKey debugging tools:")
    print("  - set_verbose(True): See chain execution")
    print("  - set_debug(True): See detailed internals")
    print("  - try/except: Handle and understand errors")
    print("  - time.time(): Measure performance")