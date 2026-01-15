# From: Zero to AI Agent, Chapter 6, Section 6.4
# File: 07_retry_logic.py
# Retry Pattern - Handling unreliable operations


import time
import random

def retry_operation(func, max_attempts=3, backoff_factor=2):
    """
    Retry a function with exponential backoff.

    This is useful for API calls that might fail temporarily.
    Each retry waits longer than the previous one.
    """
    delay = 1
    last_exception = None

    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            last_exception = e
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_attempts - 1:
                # Add jitter to prevent thundering herd
                jitter = random.uniform(0, delay * 0.1)
                wait_time = delay + jitter
                print(f"Waiting {wait_time:.1f} seconds before retry...")
                time.sleep(wait_time)
                delay *= backoff_factor

    raise last_exception


# Example: Simulating an unreliable API
def unreliable_api_call():
    """Simulates an API that fails randomly"""
    if random.random() < 0.7:  # 70% chance of failure
        raise ConnectionError("API temporarily unavailable")
    return {"status": "success", "data": "Hello from the API!"}


# Demo the retry logic
print("=" * 50)
print("RETRY PATTERN DEMO")
print("=" * 50)

try:
    result = retry_operation(unreliable_api_call, max_attempts=5)
    print(f"\nSuccess! Result: {result}")
except ConnectionError as e:
    print(f"\nAll attempts failed: {e}")


# A simpler retry approach without the helper function
print("\n" + "=" * 50)
print("SIMPLE RETRY APPROACH")
print("=" * 50)

max_attempts = 3
for attempt in range(max_attempts):
    try:
        # Your API call here
        result = unreliable_api_call()
        print(f"Success on attempt {attempt + 1}!")
        break
    except ConnectionError as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if attempt < max_attempts - 1:
            time.sleep(1)  # Wait before retry
        else:
            print("All attempts exhausted!")
