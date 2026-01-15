# From: Zero to AI Agent, Chapter 11, Section 11.7
# File: best_practices.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import logging
import os

# 1. Always handle missing variables in prompts
def safe_chain_invoke(chain, inputs):
    """Safely invoke a chain with error handling"""
    try:
        return chain.invoke(inputs)
    except KeyError as e:
        raise ValueError(
            f"Missing required input: {e}. "
            f"Please provide all required variables."
        )

# 2. Use meaningful error messages
def check_api_key(api_key):
    if not api_key:
        raise ValueError(
            "OpenAI API key not found. "
            "Please set OPENAI_API_KEY in your .env file"
        )  # Clear problem AND solution

# 3. Log important steps
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_chain_execution(input_data):
    logger.info(f"Starting chain with input: {input_data}")
    # result = chain.invoke(input_data)
    # logger.info(f"Chain completed successfully")

# 4. Test individual components
def test_components_separately():
    """Test each part of your chain individually"""
    # Test prompt alone
    prompt = ChatPromptTemplate.from_template("Test: {input}")
    assert prompt.format(input="test") == "Test: test"
    
    # Test model alone
    llm = ChatOpenAI()
    # response = llm.invoke("Test message")
    
    # Test parser alone
    parser = StrOutputParser()
    # parsed = parser.parse(response)
    
    # THEN test the full chain
    # chain = prompt | llm | parser

# 5. Keep debug code separate
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

if DEBUG_MODE:
    from langchain_core.globals import set_debug
    set_debug(True)
    print("Debug mode enabled")

# 6. Build chains incrementally
def build_robust_chain():
    """Build chains step by step with validation"""
    # Step 1: Create and validate prompt
    prompt = ChatPromptTemplate.from_template("Answer: {question}")
    
    # Step 2: Create model with fallback
    primary_llm = ChatOpenAI(model="gpt-4")
    fallback_llm = ChatOpenAI(model="gpt-3.5-turbo")
    
    # Step 3: Add parser
    parser = StrOutputParser()
    
    # Step 4: Compose with error handling
    def safe_chain(question):
        try:
            chain = prompt | primary_llm | parser
            return chain.invoke({"question": question})
        except Exception as e:
            logger.warning(f"Primary chain failed: {e}, using fallback")
            chain = prompt | fallback_llm | parser
            return chain.invoke({"question": question})
    
    return safe_chain

# 7. Monitor chain performance
import time

def monitor_chain_performance(chain, inputs):
    """Monitor and log chain performance"""
    start_time = time.time()
    
    try:
        result = chain.invoke(inputs)
        execution_time = time.time() - start_time
        
        logger.info(f"Chain executed in {execution_time:.2f} seconds")
        
        if execution_time > 10:
            logger.warning("Chain took longer than 10 seconds")
        
        return result
    except Exception as e:
        logger.error(f"Chain failed after {time.time() - start_time:.2f} seconds: {e}")
        raise