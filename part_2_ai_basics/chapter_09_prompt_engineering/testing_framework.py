# From: Zero to AI Agent, Chapter 9, Section 9.5
# File: testing_framework.py

"""
Simple framework for testing prompts systematically
"""

def test_prompt(prompt_template, test_cases, model="gpt-3.5-turbo"):
    """Test a prompt with multiple inputs"""
    results = []
    
    for test_input in test_cases:
        prompt = prompt_template.format(input=test_input)
        
        # In real implementation: call API
        # response = get_ai_response(prompt, model)
        
        result = {
            "input": test_input,
            "prompt": prompt,
            "response": "AI response here",
            "score": evaluate_response()  # Your scoring function
        }
        results.append(result)
    
    return results

def evaluate_response():
    """Placeholder for response evaluation"""
    # Implement your scoring logic here
    return 8.0

# Track iterations
iteration_history = {
    "v1": {
        "prompt": "Summarize: {input}",
        "avg_score": 6.2,
        "issues": ["Too vague", "Inconsistent length"]
    },
    "v2": {
        "prompt": "Summarize in 3 bullets: {input}",
        "avg_score": 7.8,
        "issues": ["No audience context"]
    },
    "v3": {
        "prompt": "Executive summary, 3 key points: {input}",
        "avg_score": 9.1,
        "issues": ["Minor format inconsistencies"]
    }
}

if __name__ == "__main__":
    print("PROMPT TESTING FRAMEWORK")
    print("="*50)
    print("This framework helps you:")
    print("1. Test prompts systematically")
    print("2. Track iteration history")
    print("3. Measure improvement objectively")
    print("\nCurrent iterations tracked:", len(iteration_history))
    print("Best performing version:", max(iteration_history.items(), 
          key=lambda x: x[1]['avg_score'])[0])