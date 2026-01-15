# From: Zero to AI Agent, Chapter 7, Section 7.7
# File: context_management.py

"""
Managing conversation context to avoid the hidden cost trap.
Shows the difference between bad and good context management.
"""

from typing import List, Dict
import time


def bad_context_accumulation():
    """
    ❌ BAD: Context grows with each message, costs grow quadratically!
    This is a common mistake that can make costs explode.
    """
    print("="*60)
    print("❌ BAD EXAMPLE: Uncontrolled Context Growth")
    print("="*60)
    
    messages = []
    total_tokens = 0
    
    # Simulate 100 message exchanges
    for i in range(20):  # Using 20 for demo, imagine 100+
        # Add user message
        messages.append({"role": "user", "content": f"Message {i}"})
        
        # Each API call includes ALL previous messages!
        tokens_in_request = sum(len(m["content"]) for m in messages) * 5  # Rough token estimate
        total_tokens += tokens_in_request
        
        print(f"Message {i+1}: Sending {len(messages)} messages ({tokens_in_request} tokens)")
        
        # Add assistant response (simulated)
        messages.append({"role": "assistant", "content": f"Response {i}"})
    
    print(f"\nTotal tokens sent: {total_tokens}")
    print(f"Average tokens per request: {total_tokens/20:.0f}")
    print("⚠️ Notice how token count grows with each message!")
    
    # Calculate approximate cost
    cost_per_1k = 0.002  # GPT-3.5-turbo average
    total_cost = (total_tokens / 1000) * cost_per_1k
    print(f"Estimated cost: ${total_cost:.4f}")
    
    return total_tokens


def good_context_management():
    """
    ✅ GOOD: Manage context size to keep costs under control
    """
    print("\n" + "="*60)
    print("✅ GOOD EXAMPLE: Managed Context")
    print("="*60)
    
    messages = []
    total_tokens = 0
    max_context_tokens = 2000  # Set a limit
    
    for i in range(20):
        # Add user message
        messages.append({"role": "user", "content": f"Message {i}"})
        
        # Manage context size BEFORE making API call
        messages = manage_context(messages, max_tokens=max_context_tokens)
        
        tokens_in_request = sum(len(m["content"]) for m in messages) * 5
        total_tokens += tokens_in_request
        
        print(f"Message {i+1}: Sending {len(messages)} messages ({tokens_in_request} tokens)")
        
        # Add assistant response
        messages.append({"role": "assistant", "content": f"Response {i}"})
    
    print(f"\nTotal tokens sent: {total_tokens}")
    print(f"Average tokens per request: {total_tokens/20:.0f}")
    print("✅ Token count stays controlled!")
    
    # Calculate cost
    cost_per_1k = 0.002
    total_cost = (total_tokens / 1000) * cost_per_1k
    print(f"Estimated cost: ${total_cost:.4f}")
    
    return total_tokens


def manage_context(messages: List[Dict], max_tokens: int = 2000) -> List[Dict]:
    """
    Keep context under control by removing old messages
    
    Args:
        messages: List of message dictionaries
        max_tokens: Maximum tokens to keep in context
    
    Returns:
        Trimmed message list
    """
    # Always keep system message if present
    has_system = messages and messages[0].get("role") == "system"
    start_index = 1 if has_system else 0
    
    # Estimate total tokens (rough: 1 token ≈ 4 characters)
    def estimate_tokens(msgs):
        return sum(len(m.get("content", "")) / 4 for m in msgs)
    
    total_tokens = estimate_tokens(messages)
    
    # Remove oldest messages if over limit
    while total_tokens > max_tokens and len(messages) > start_index + 2:
        # Remove oldest user-assistant pair (keep system message)
        messages.pop(start_index)  # Remove oldest user message
        if start_index < len(messages) and messages[start_index].get("role") == "assistant":
            messages.pop(start_index)  # Remove corresponding assistant message
        
        total_tokens = estimate_tokens(messages)
    
    return messages


def smart_context_strategies():
    """
    Advanced context management strategies
    """
    print("\n" + "="*60)
    print("SMART CONTEXT MANAGEMENT STRATEGIES")
    print("="*60)
    
    strategies = {
        "Sliding Window": {
            "description": "Keep only last N messages",
            "pros": "Simple, predictable cost",
            "cons": "Loses older context",
            "code": """
messages = messages[-10:]  # Keep last 10 messages
            """
        },
        "Summarization": {
            "description": "Periodically summarize old messages",
            "pros": "Preserves key information",
            "cons": "Requires extra API call for summary",
            "code": """
if len(messages) > 20:
    summary = summarize_messages(messages[:-10])
    messages = [{"role": "system", "content": summary}] + messages[-10:]
            """
        },
        "Importance Scoring": {
            "description": "Keep only important messages",
            "pros": "Retains critical context",
            "cons": "Complex to implement",
            "code": """
messages = [m for m in messages if m.get('importance', 0) > threshold]
            """
        },
        "Token Budget": {
            "description": "Allocate token budget per conversation turn",
            "pros": "Precise cost control",
            "cons": "May cut off mid-conversation",
            "code": """
while calculate_tokens(messages) > budget:
    messages.pop(1)  # Remove oldest after system
            """
        }
    }
    
    for name, strategy in strategies.items():
        print(f"\n📋 {name}:")
        print(f"  Description: {strategy['description']}")
        print(f"  ✅ Pros: {strategy['pros']}")
        print(f"  ❌ Cons: {strategy['cons']}")
        print(f"  Code snippet:{strategy['code']}")


def safe_retry_pattern():
    """
    Safe retry pattern that avoids infinite cost loops
    """
    print("\n" + "="*60)
    print("SAFE RETRY PATTERNS")
    print("="*60)
    
    # ❌ BAD: Infinite retries
    print("\n❌ BAD: Infinite retry loop")
    print("-" * 40)
    print("""
while True:
    try:
        response = expensive_api_call()
        break
    except:
        continue  # This could run forever!
""")
    
    # ✅ GOOD: Limited retries with backoff
    print("\n✅ GOOD: Limited retries with exponential backoff")
    print("-" * 40)
    
    def safe_api_call(max_retries=3):
        """Safe API call with limited retries and backoff"""
        for attempt in range(max_retries):
            try:
                # Simulate API call
                if attempt < 2:  # Simulate failures
                    raise Exception("API Error")
                return {"success": True, "attempt": attempt + 1}
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"  Failed after {max_retries} attempts")
                    raise
                
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"  Attempt {attempt + 1} failed, waiting {wait_time}s...")
                time.sleep(wait_time)
        
        return None
    
    # Demonstrate
    print("\nDemonstration:")
    try:
        result = safe_api_call()
        print(f"  Success on attempt {result['attempt']}")
    except:
        print("  Final failure - stopping to prevent cost overrun")


class ContextWindowManager:
    """
    Professional context window management
    """
    
    def __init__(self, max_tokens: int = 4000, reserve_tokens: int = 500):
        """
        Initialize context manager
        
        Args:
            max_tokens: Maximum context window size
            reserve_tokens: Tokens to reserve for response
        """
        self.max_tokens = max_tokens
        self.reserve_tokens = reserve_tokens
        self.effective_max = max_tokens - reserve_tokens
        self.total_trimmed = 0
        self.trim_count = 0
    
    def prepare_context(self, messages: List[Dict], new_message: str) -> List[Dict]:
        """
        Prepare context for API call
        
        Args:
            messages: Current conversation history
            new_message: New message to add
        
        Returns:
            Optimized message list within token budget
        """
        # Add new message temporarily
        temp_messages = messages + [{"role": "user", "content": new_message}]
        
        # Calculate current size
        current_tokens = self._estimate_tokens(temp_messages)
        
        if current_tokens <= self.effective_max:
            return temp_messages
        
        # Need to trim
        self.trim_count += 1
        tokens_to_trim = current_tokens - self.effective_max
        self.total_trimmed += tokens_to_trim
        
        # Trim strategy: Remove oldest messages but keep system
        trimmed = self._trim_messages(temp_messages, self.effective_max)
        
        print(f"🔄 Trimmed context: {current_tokens} → {self._estimate_tokens(trimmed)} tokens")
        
        return trimmed
    
    def _estimate_tokens(self, messages: List[Dict]) -> int:
        """Estimate token count"""
        return sum(len(m.get("content", "")) // 4 for m in messages)
    
    def _trim_messages(self, messages: List[Dict], target_tokens: int) -> List[Dict]:
        """Trim messages to fit within token budget"""
        # Keep system message if present
        result = []
        if messages and messages[0].get("role") == "system":
            result.append(messages[0])
            messages = messages[1:]
        
        # Keep most recent messages that fit
        for msg in reversed(messages):
            test_result = [msg] + result[1:] if result else [msg]
            if self._estimate_tokens(result[:1] + test_result) <= target_tokens:
                result = result[:1] + test_result if result else test_result
            else:
                break
        
        return result
    
    def get_stats(self) -> Dict:
        """Get context management statistics"""
        return {
            "max_tokens": self.max_tokens,
            "reserve_tokens": self.reserve_tokens,
            "effective_max": self.effective_max,
            "total_trimmed": self.total_trimmed,
            "trim_count": self.trim_count,
            "avg_trimmed": self.total_trimmed / max(1, self.trim_count)
        }


def demonstrate_context_costs():
    """
    Show the real cost impact of context management
    """
    print("\n" + "="*60)
    print("COST IMPACT COMPARISON")
    print("="*60)
    
    bad_tokens = bad_context_accumulation()
    good_tokens = good_context_management()
    
    savings = bad_tokens - good_tokens
    savings_percent = (savings / bad_tokens) * 100
    
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    print(f"Bad approach: {bad_tokens:,} tokens")
    print(f"Good approach: {good_tokens:,} tokens")
    print(f"Tokens saved: {savings:,} ({savings_percent:.1f}%)")
    
    # Cost calculation
    cost_per_1k = 0.002
    money_saved = (savings / 1000) * cost_per_1k
    print(f"Money saved on 20 messages: ${money_saved:.4f}")
    print(f"Projected monthly savings (1000 conversations): ${money_saved * 50:.2f}")


if __name__ == "__main__":
    # Demonstrate the cost difference
    demonstrate_context_costs()
    
    # Show strategies
    smart_context_strategies()
    
    # Show safe retry pattern
    safe_retry_pattern()
    
    # Professional context manager demo
    print("\n" + "="*60)
    print("PROFESSIONAL CONTEXT MANAGER DEMO")
    print("="*60)
    
    manager = ContextWindowManager(max_tokens=2000)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]
    
    # Simulate conversation
    for i in range(10):
        new_msg = f"This is message {i} with some content to simulate real conversation length."
        messages = manager.prepare_context(messages[:-1] if i > 0 else messages, new_msg)
        messages.append({"role": "assistant", "content": f"Response to message {i}"})
    
    stats = manager.get_stats()
    print("\nContext Manager Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
