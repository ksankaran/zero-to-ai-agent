# From: Zero to AI Agent, Chapter 11, Section 11.1
# File: exercise_3_11_1_solution.py

# Chapter 8 Challenges and LangChain Solutions

challenges = {
    "1. Managing Message History": {
        "Chapter 8 Problem": """
        messages = []
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "assistant", "content": response})
        # Manual management, easy to mess up formatting
        """,
        "LangChain Solution": """
        from langchain.memory import ConversationBufferMemory
        memory = ConversationBufferMemory()
        memory.save_context({"input": user_msg}, {"output": ai_response})
        # Automatic management, consistent format
        """
    },
    
    "2. Handling Different Message Formats": {
        "Chapter 8 Problem": """
        # OpenAI format
        {"role": "system", "content": "..."}
        # Anthropic format different
        # Google format different again
        """,
        "LangChain Solution": """
        from langchain.schema import SystemMessage, HumanMessage
        # Same format works for all providers!
        """
    },
    
    "3. Error Handling": {
        "Chapter 8 Problem": """
        try:
            response = openai.ChatCompletion.create(...)
        except openai.error.APIError:
            # Handle API errors
        except openai.error.RateLimitError:
            # Handle rate limits
        # Different errors for each provider
        """,
        "LangChain Solution": """
        from langchain.callbacks import RetryWithErrorHandler
        # Unified error handling across all providers
        """
    },
    
    "4. Switching Between Models": {
        "Chapter 8 Problem": """
        # Had to rewrite code for different models
        if use_gpt4:
            model = "gpt-4"
            # Different parameters
        else:
            model = "gpt-3.5-turbo"
            # Different handling
        """,
        "LangChain Solution": """
        llm = ChatOpenAI(model=model_name)
        # Same interface for all models
        """
    },
    
    "5. Prompt Management": {
        "Chapter 8 Problem": """
        system_prompt = "You are a helpful assistant..."
        user_prompt = f"User said: {input}"
        # Strings everywhere, hard to maintain
        """,
        "LangChain Solution": """
        from langchain.prompts import ChatPromptTemplate
        prompt = ChatPromptTemplate.from_template("...")
        # Reusable, testable, maintainable
        """
    }
}

def demonstrate_improvement():
    """Show how LangChain simplifies each challenge"""
    
    print("🎯 How LangChain Solves Chapter 8 Challenges\n")
    
    for challenge, details in challenges.items():
        print(f"{challenge}")
        print("-" * 40)
        print("❌ Chapter 8 Approach:")
        print(details["Chapter 8 Problem"])
        print("\n✅ LangChain Approach:")
        print(details["LangChain Solution"])
        print("\n")

if __name__ == "__main__":
    demonstrate_improvement()
