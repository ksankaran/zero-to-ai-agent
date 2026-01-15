# From: Zero to AI Agent, Chapter 8, Section 8.3
# File: exercise_3_8_3_model_comparison.py

import openai
from pathlib import Path
import json

def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

def compare_models(client, prompt, models):
    """Compare responses from different models"""
    results = {}
    
    for model in models:
        try:
            print(f"\n🤖 Testing {model}...")
            
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=150  # Limit for fair comparison
            )
            
            results[model] = {
                'response': response.choices[0].message.content,
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
                'finish_reason': response.choices[0].finish_reason
            }
            
            # Calculate cost based on model
            if 'gpt-3.5' in model:
                cost = response.usage.total_tokens * 0.002 / 1000
            elif 'gpt-4' in model:
                cost = response.usage.total_tokens * 0.03 / 1000
            else:
                cost = 0
            
            results[model]['cost'] = cost
            print(f"✅ Success!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results[model] = {'error': str(e)}
    
    return results

# Setup
api_key = load_api_key()
client = openai.OpenAI(api_key=api_key)

# Models to compare (use what's available to you)
models = ["gpt-3.5-turbo"]  # Add more models if you have access

# You can try adding these if you have access:
# models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"]

print("🔬 Model Comparison Tool")
print("=" * 50)
print(f"Available models to test: {', '.join(models)}")
print("Type 'quit' to exit, 'test' for preset tests")
print("-" * 50)

comparison_history = []

while True:
    prompt = input("\nEnter prompt to compare (or command): ").strip()
    
    if prompt.lower() == 'quit':
        # Save comparison history
        if comparison_history:
            filename = "model_comparisons.json"
            with open(filename, 'w') as f:
                json.dump(comparison_history, f, indent=2)
            print(f"\n💾 Saved {len(comparison_history)} comparisons to {filename}")
        break
    
    if prompt.lower() == 'test':
        # Preset test prompts
        test_prompts = [
            "Write a haiku about coding",
            "Explain recursion in one sentence",
            "What's the meaning of life?"
        ]
        
        for test_prompt in test_prompts:
            print(f"\n📝 Test: '{test_prompt}'")
            results = compare_models(client, test_prompt, models)
            
            # Display results
            for model, data in results.items():
                if 'error' not in data:
                    print(f"\n{model}:")
                    print(f"  Response: {data['response'][:100]}...")
                    print(f"  Tokens: {data['total_tokens']}")
                    print(f"  Cost: ${data['cost']:.6f}")
        continue
    
    # Compare models for user prompt
    results = compare_models(client, prompt, models)
    
    # Display comparison
    print("\n" + "=" * 50)
    print("📊 COMPARISON RESULTS")
    print("=" * 50)
    
    for model, data in results.items():
        print(f"\n🤖 {model}:")
        
        if 'error' in data:
            print(f"  ❌ Error: {data['error']}")
        else:
            print(f"  💬 Response: {data['response']}")
            print(f"  📊 Tokens Used:")
            print(f"     Prompt: {data['prompt_tokens']}")
            print(f"     Response: {data['completion_tokens']}")
            print(f"     Total: {data['total_tokens']}")
            print(f"  💰 Cost: ${data['cost']:.6f}")
            print(f"  🏁 Finish: {data['finish_reason']}")
    
    # Analysis
    valid_results = {k: v for k, v in results.items() if 'error' not in v}
    
    if len(valid_results) > 1:
        print("\n📈 Analysis:")
        
        # Find cheapest
        cheapest = min(valid_results.items(), key=lambda x: x[1]['cost'])
        print(f"  💰 Cheapest: {cheapest[0]} (${cheapest[1]['cost']:.6f})")
        
        # Find most verbose
        most_verbose = max(valid_results.items(), key=lambda x: x[1]['completion_tokens'])
        print(f"  📝 Most detailed: {most_verbose[0]} ({most_verbose[1]['completion_tokens']} tokens)")
        
        # Calculate cost difference
        costs = [v['cost'] for v in valid_results.values()]
        if len(costs) > 1:
            cost_diff = max(costs) - min(costs)
            print(f"  💵 Cost difference: ${cost_diff:.6f}")
    
    # Save to history
    comparison_history.append({
        'prompt': prompt,
        'results': results
    })

print("\n👋 Thanks for using Model Comparison Tool!")
print("💡 Tip: GPT-3.5-turbo is usually best for simple tasks (fast & cheap)")
print("     GPT-4 is better for complex reasoning (slower & more expensive)")
