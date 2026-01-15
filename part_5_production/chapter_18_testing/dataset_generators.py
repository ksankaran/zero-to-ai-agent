# From: AI Agents Book, Chapter 18, Section 18.4
# File: dataset_generators.py
# Description: Tools for generating synthetic test datasets

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def generate_variations(original_query: str, llm, count: int = 5) -> list[str]:
    """
    Generate phrasing variations of a query.
    
    Takes a single query and generates multiple phrasings that mean the same thing.
    Useful for testing that your agent handles different phrasings consistently.
    
    Args:
        original_query: The original user query
        llm: A language model to generate variations
        count: Number of variations to generate
    
    Returns:
        List of query variations
    """
    prompt = f"""Generate {count} different ways a user might ask this same question.
Vary the formality, length, and phrasing while keeping the meaning identical.

Original: {original_query}

Variations (one per line, numbered):"""
    
    response = llm.invoke(prompt)
    
    # Parse the numbered list from response
    variations = []
    for line in response.content.split('\n'):
        line = line.strip()
        if line and len(line) > 2:
            # Remove numbering like "1.", "1)", "1:"
            if line[0].isdigit():
                # Find where the actual text starts
                for i, char in enumerate(line):
                    if char in '.):' and i < 3:
                        line = line[i+1:].strip()
                        break
            if line:
                variations.append(line)
    
    return variations[:count]


def generate_scenario_cases(scenario_description: str, count: int, llm) -> list[dict]:
    """
    Generate test cases for a specific scenario.
    
    Args:
        scenario_description: Description of the scenario to generate cases for
        count: Number of test cases to generate
        llm: A language model to generate cases
    
    Returns:
        List of test case dictionaries with 'query' and 'should_address' keys
    """
    prompt = f"""Generate {count} realistic user queries for this scenario:
{scenario_description}

For each query, also provide what a correct response should address.

Format each as:
QUERY: [the user's question]
SHOULD_ADDRESS: [key points the response must cover]

Generate {count} different cases:"""
    
    response = llm.invoke(prompt)
    
    # Parse into structured cases
    cases = []
    current_query = None
    current_should_address = None
    
    for line in response.content.split('\n'):
        line = line.strip()
        if line.startswith('QUERY:'):
            if current_query and current_should_address:
                cases.append({
                    'query': current_query,
                    'should_address': current_should_address
                })
            current_query = line[6:].strip()
            current_should_address = None
        elif line.startswith('SHOULD_ADDRESS:'):
            current_should_address = line[15:].strip()
    
    # Don't forget the last case
    if current_query and current_should_address:
        cases.append({
            'query': current_query,
            'should_address': current_should_address
        })
    
    return cases[:count]


def generate_edge_cases(llm, edge_type: str = "ambiguous") -> list[str]:
    """
    Generate edge case queries for testing robustness.
    
    Args:
        llm: A language model to generate cases
        edge_type: Type of edge case to generate
    
    Returns:
        List of edge case queries
    """
    edge_case_prompts = {
        "ambiguous": "Generate 5 queries where the user's intent is ambiguous and could be interpreted multiple ways",
        "multi_request": "Generate 5 queries that combine multiple unrelated requests in a single message",
        "typos": "Generate 5 queries with realistic typos and grammatical errors",
        "out_of_scope": "Generate 5 queries that are just barely outside a typical customer service agent's scope",
        "boundary": "Generate 5 queries that test the boundaries between different categories (e.g., is this a billing question or a technical question?)",
    }
    
    prompt = edge_case_prompts.get(edge_type, edge_case_prompts["ambiguous"])
    prompt += "\n\nList each query on its own line:"
    
    response = llm.invoke(prompt)
    
    # Parse into list
    cases = []
    for line in response.content.split('\n'):
        line = line.strip()
        if line and len(line) > 10:  # Filter out empty/short lines
            # Remove numbering
            if line[0].isdigit() and len(line) > 3:
                for i, char in enumerate(line):
                    if char in '.):' and i < 3:
                        line = line[i+1:].strip()
                        break
            if line:
                cases.append(line)
    
    return cases[:5]


def generate_adversarial_cases(llm) -> dict[str, list[str]]:
    """
    Generate a suite of adversarial test cases.
    
    Returns:
        Dictionary mapping adversarial category to list of test queries
    """
    categories = {
        "ambiguity": "Generate queries where the correct answer is 'I need more information' because key details are missing",
        "boundary": "Generate queries at the edge of a customer service agent's capabilities - almost but not quite in scope",
        "consistency": "Generate 5 different phrasings of the same factual question to test for consistent answers",
    }
    
    results = {}
    for category, prompt in categories.items():
        full_prompt = f"{prompt}\n\nList 5 examples, one per line:"
        response = llm.invoke(full_prompt)
        
        cases = []
        for line in response.content.split('\n'):
            line = line.strip()
            if line and len(line) > 10:
                if line[0].isdigit():
                    for i, char in enumerate(line):
                        if char in '.):' and i < 3:
                            line = line[i+1:].strip()
                            break
                if line:
                    cases.append(line)
        
        results[category] = cases[:5]
    
    return results


# Example usage
if __name__ == "__main__":
    from langchain_openai import ChatOpenAI
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    
    # Generate variations
    print("=== Query Variations ===")
    original = "How do I reset my password?"
    variations = generate_variations(original, llm)
    print(f"Original: {original}")
    for i, var in enumerate(variations, 1):
        print(f"  {i}. {var}")
    
    # Generate scenario cases
    print("\n=== Scenario Cases ===")
    scenario = "A user is frustrated because their order hasn't arrived after 2 weeks"
    cases = generate_scenario_cases(scenario, 3, llm)
    for case in cases:
        print(f"Query: {case['query']}")
        print(f"Should address: {case['should_address']}\n")
    
    # Generate edge cases
    print("=== Edge Cases (Ambiguous) ===")
    edge_cases = generate_edge_cases(llm, "ambiguous")
    for case in edge_cases:
        print(f"  - {case}")
