# From: Zero to AI Agent, Chapter 10, Section 10.1
# File: chatbot_vs_agent_demo.py

"""
Demonstration of the fundamental difference between chatbots and agents.
This shows how chatbots respond to questions while agents solve problems.
"""

def chatbot_weather():
    """
    CHATBOT: One question, one answer approach.
    Limited to generating text responses without real data access.
    """
    user_input = "What's the weather like?"
    response = "I don't have access to current weather data, but I can tell you typical patterns..."
    return response


def agent_weather_concept():
    """
    AGENT: Observes, decides, acts, completes.
    This is conceptual - showing how an agent would think through the problem.
    In a real implementation, these would be actual tool calls.
    """
    task = "Tell user about weather"
    
    # Agent's internal thought process (this happens internally!)
    thought_process = [
        "User wants weather information",
        "Check available tools -> found weather_api",
        "Need location first -> detect_location()",
        "Location found: New York",
        "Call weather_api('New York') -> 72°F, Sunny",
        "Check user preferences -> prefers Celsius",
        "Convert 72°F to 22°C",
        "Check calendar -> user has outdoor meeting at 2pm",
        "Add relevant context to response"
    ]
    
    # Agent's enhanced response after processing
    response = "It's currently 22°C and sunny in New York. Perfect weather for your 2pm outdoor meeting! Consider bringing sunglasses."
    
    # In a real agent, additional actions might include:
    additional_actions = [
        "Notice user has outdoor meeting scheduled",
        "Suggest bringing sunglasses",
        "Check UV index for sun protection reminder"
    ]
    
    return {
        "task": task,
        "thought_process": thought_process,
        "response": response,
        "additional_context": additional_actions
    }


def demonstrate_difference():
    """
    Show the difference between chatbot and agent approaches.
    """
    print("=" * 60)
    print("CHATBOT vs AGENT: Weather Query Example")
    print("=" * 60)
    
    # Chatbot approach
    print("\n🤖 CHATBOT APPROACH:")
    print("-" * 30)
    print("User: What's the weather like?")
    chatbot_response = chatbot_weather()
    print(f"Chatbot: {chatbot_response}")
    print("Result: Answers the literal question with limited information")
    
    # Agent approach
    print("\n🎯 AGENT APPROACH:")
    print("-" * 30)
    print("User: What's the weather like?")
    agent_result = agent_weather_concept()
    
    print("\nAgent's Internal Process:")
    for step in agent_result["thought_process"][:5]:  # Show first 5 steps
        print(f"  → {step}")
    print("  → ... (continues processing)")
    
    print(f"\nAgent: {agent_result['response']}")
    print("\nResult: Solves the underlying need with context and actionable information")
    
    # Key differences
    print("\n" + "=" * 60)
    print("KEY DIFFERENCES:")
    print("-" * 30)
    print("✓ Chatbot: Answers the question")
    print("✓ Agent: Solves the underlying need")
    print("\n✓ Chatbot: Single response based on training")
    print("✓ Agent: Multiple steps with tool usage")
    print("\n✓ Chatbot: No real-world data access")
    print("✓ Agent: Integrates multiple data sources")
    print("\n✓ Chatbot: Generic response")
    print("✓ Agent: Personalized with context")


if __name__ == "__main__":
    demonstrate_difference()
    
    print("\n" + "=" * 60)
    print("💡 This is a conceptual demonstration.")
    print("In Chapter 11, you'll build real agents with actual tool integration!")