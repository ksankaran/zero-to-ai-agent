# From: Zero to AI Agent, Chapter 8, Section 8.3
# File: exercise_1_8_3_token_predictor.py

import openai
from pathlib import Path

def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

def predict_tokens(text):
    """Predict token count using different methods"""
    # Method 1: Characters divided by 4
    char_estimate = len(text) // 4
    
    # Method 2: Words times 1.3
    word_estimate = int(len(text.split()) * 1.3)
    
    # Method 3: Average of both
    avg_estimate = (char_estimate + word_estimate) // 2
    
    return {
        'char_method': char_estimate,
        'word_method': word_estimate,
        'average': avg_estimate
    }

# Setup
api_key = load_api_key()
client = openai.OpenAI(api_key=api_key)

# Track accuracy
predictions = []
actuals = []

print("🎯 Token Predictor Challenge")
print("=" * 50)
print("I'll predict token counts - let's see how accurate I am!")
print("Type 'quit' to exit, 'score' to see accuracy")
print("-" * 50)

while True:
    prompt = input("\nEnter prompt: ").strip()
    
    if prompt.lower() == 'quit':
        break
    
    if prompt.lower() == 'score':
        if predictions:
            # Calculate accuracy
            errors = [abs(p - a) for p, a in zip(predictions, actuals)]
            avg_error = sum(errors) / len(errors)
            accuracy = max(0, 100 - (avg_error * 2))  # Rough accuracy score
            
            print(f"\n📊 Your Prediction Score:")
            print(f"  Predictions made: {len(predictions)}")
            print(f"  Average error: {avg_error:.1f} tokens")
            print(f"  Accuracy score: {accuracy:.1f}%")
            
            if accuracy > 80:
                print("  🏆 Excellent predictor!")
            elif accuracy > 60:
                print("  👍 Good job!")
            else:
                print("  📚 Keep practicing!")
        else:
            print("No predictions yet!")
        continue
    
    # Get predictions
    estimates = predict_tokens(prompt)
    
    print(f"\n📏 My predictions:")
    print(f"  Character method: {estimates['char_method']} tokens")
    print(f"  Word method: {estimates['word_method']} tokens")
    print(f"  Best guess: {estimates['average']} tokens")
    
    # Make API call
    print("\n🔄 Checking with API...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Get actual counts
    actual_prompt_tokens = response.usage.prompt_tokens
    actual_completion_tokens = response.usage.completion_tokens
    
    print(f"\n✅ Actual results:")
    print(f"  Prompt tokens: {actual_prompt_tokens}")
    print(f"  Response tokens: {actual_completion_tokens}")
    print(f"  Total: {response.usage.total_tokens}")
    
    # Calculate accuracy for this prediction
    error = abs(estimates['average'] - actual_prompt_tokens)
    
    if error <= 2:
        print(f"  🎯 Excellent! Only {error} tokens off!")
    elif error <= 5:
        print(f"  👍 Good! {error} tokens off")
    else:
        print(f"  😅 {error} tokens off - tokens are tricky!")
    
    # Track for scoring
    predictions.append(estimates['average'])
    actuals.append(actual_prompt_tokens)
    
    # Show the response
    print(f"\n💬 Response: {response.choices[0].message.content[:100]}...")

# Final score
if predictions:
    errors = [abs(p - a) for p, a in zip(predictions, actuals)]
    avg_error = sum(errors) / len(errors)
    
    print(f"\n🏁 Final Score:")
    print(f"  Total predictions: {len(predictions)}")
    print(f"  Average error: {avg_error:.1f} tokens")
    print(f"  Tip: Tokens roughly = max(chars/4, words*1.3)")

print("\n👋 Thanks for playing Token Predictor!")
