# From: Zero to AI Agent, Chapter 8, Section 8.3
# File: exercise_2_8_3_response_timer.py

import openai
import time
from pathlib import Path

def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

def time_api_call(client, prompt):
    """Time how long an API call takes"""
    start_time = time.time()
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    return response, elapsed

# Setup
api_key = load_api_key()
client = openai.OpenAI(api_key=api_key)

# Test prompts of different lengths
test_prompts = [
    ("Short", "Hi"),
    ("Medium", "Write a haiku about programming"),
    ("Long", "Explain the theory of relativity in detail, including both special and general relativity"),
    ("Very Long", "Write a detailed essay about the history of computers, starting from Charles Babbage's Analytical Engine, through the development of ENIAC, the invention of the transistor, the rise of personal computers, and ending with modern smartphones and cloud computing. Include key figures and dates."),
]

print("⏱️ Response Time Tracker")
print("=" * 50)
print("Testing how prompt length affects response time...\n")

results = []

for name, prompt in test_prompts:
    print(f"📝 Testing {name} prompt ({len(prompt)} characters)...")
    
    # Run 3 times and average
    times = []
    tokens_list = []
    
    for i in range(3):
        response, elapsed = time_api_call(client, prompt)
        times.append(elapsed)
        tokens_list.append(response.usage.total_tokens)
        print(f"  Run {i+1}: {elapsed:.2f} seconds")
    
    avg_time = sum(times) / len(times)
    avg_tokens = sum(tokens_list) / len(tokens_list)
    
    results.append({
        'name': name,
        'prompt_length': len(prompt),
        'avg_time': avg_time,
        'avg_tokens': avg_tokens,
        'tokens_per_second': avg_tokens / avg_time if avg_time > 0 else 0
    })
    
    print(f"  Average: {avg_time:.2f} seconds for {avg_tokens:.0f} tokens")
    print()

# Analysis
print("=" * 50)
print("📊 Analysis Results:\n")

for r in results:
    print(f"{r['name']} Prompt:")
    print(f"  Length: {r['prompt_length']} chars")
    print(f"  Time: {r['avg_time']:.2f} seconds")
    print(f"  Tokens: {r['avg_tokens']:.0f}")
    print(f"  Speed: {r['tokens_per_second']:.0f} tokens/second")
    print()

# Find sweet spot
print("💡 Findings:")
print("-" * 30)

# Check if time increases with length
times = [r['avg_time'] for r in results]
if times[-1] > times[0] * 1.5:
    print("✓ Longer prompts do take more time")
else:
    print("✓ Response time is fairly consistent")

# Find best efficiency
best_efficiency = max(results, key=lambda x: x['tokens_per_second'])
print(f"✓ Best efficiency: {best_efficiency['name']} prompts")
print(f"  ({best_efficiency['tokens_per_second']:.0f} tokens/second)")

# Recommendations
print("\n🎯 Sweet Spot:")
medium_results = [r for r in results if r['prompt_length'] > 10 and r['prompt_length'] < 200]
if medium_results:
    print("Medium-length prompts (10-200 chars) offer the best balance:")
    print("- Fast response times")
    print("- Meaningful responses")
    print("- Cost-effective token usage")

print("\n⚡ Speed Tip: Response time depends more on response length than prompt length!")
