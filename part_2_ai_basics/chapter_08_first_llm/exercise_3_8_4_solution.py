# From: Zero to AI Agent, Chapter 8, Section 8.4
# File: exercise_3_8_4_circuit_breaker.py

import openai
from pathlib import Path
import time
from enum import Enum
from datetime import datetime, timedelta

def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

class CircuitState(Enum):
    CLOSED = "🟢 CLOSED"      # Normal operation
    OPEN = "🔴 OPEN"          # Blocking requests
    HALF_OPEN = "🟡 HALF-OPEN"  # Testing recovery

class CircuitBreaker:
    """Circuit breaker pattern for API calls"""
    
    def __init__(self, client, failure_threshold=3, recovery_timeout=30, success_threshold=2):
        self.client = client
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout  # seconds
        self.success_threshold = success_threshold
        self.last_failure_time = None
        self.total_requests = 0
        self.blocked_requests = 0
        self.state_history = []
    
    def call(self, messages):
        """Make API call through circuit breaker"""
        self.total_requests += 1
        
        # Check circuit state
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._change_state(CircuitState.HALF_OPEN)
                print("🔄 Circuit switching to HALF-OPEN - testing recovery...")
            else:
                self.blocked_requests += 1
                time_left = self.recovery_timeout - (datetime.now() - self.last_failure_time).seconds
                return None, f"Circuit OPEN - wait {time_left} seconds"
        
        # Try the call
        try:
            print(f"📡 Making request (Circuit: {self.state.value})...")
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                timeout=10  # Short timeout for testing
            )
            
            self._on_success()
            return response.choices[0].message.content, None
            
        except Exception as e:
            self._on_failure(e)
            return None, f"Request failed: {type(e).__name__}"
    
    def _should_attempt_reset(self):
        """Check if enough time has passed to try recovery"""
        if self.last_failure_time:
            elapsed = (datetime.now() - self.last_failure_time).seconds
            return elapsed >= self.recovery_timeout
        return False
    
    def _on_success(self):
        """Handle successful request"""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            print(f"✅ Success in HALF-OPEN ({self.success_count}/{self.success_threshold})")
            
            if self.success_count >= self.success_threshold:
                # Fully recover
                self._change_state(CircuitState.CLOSED)
                self.failure_count = 0
                self.success_count = 0
                print("🎉 Circuit CLOSED - fully recovered!")
        else:
            # Reset failure count on success in CLOSED state
            self.failure_count = 0
    
    def _on_failure(self, error):
        """Handle failed request"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        print(f"❌ Failure #{self.failure_count}: {type(error).__name__}")
        
        if self.state == CircuitState.HALF_OPEN:
            # Single failure in HALF-OPEN goes back to OPEN
            self._change_state(CircuitState.OPEN)
            self.success_count = 0
            print("⚠️ Recovery failed - circuit OPEN again")
            
        elif self.failure_count >= self.failure_threshold:
            # Too many failures - open the circuit
            self._change_state(CircuitState.OPEN)
            print(f"🔴 Circuit OPEN after {self.failure_count} failures!")
    
    def _change_state(self, new_state):
        """Change state and record history"""
        old_state = self.state
        self.state = new_state
        self.state_history.append({
            'from': old_state.value,
            'to': new_state.value,
            'timestamp': datetime.now().isoformat()
        })
        # Keep only last 10 state changes
        self.state_history = self.state_history[-10:]
    
    def get_status(self):
        """Get circuit breaker status"""
        return {
            'state': self.state.value,
            'failures': self.failure_count,
            'successes': self.success_count,
            'total_requests': self.total_requests,
            'blocked_requests': self.blocked_requests,
            'recovery_in': self._time_to_recovery(),
            'state_changes': len(self.state_history)
        }
    
    def _time_to_recovery(self):
        """Calculate time until recovery attempt"""
        if self.state == CircuitState.OPEN and self.last_failure_time:
            elapsed = (datetime.now() - self.last_failure_time).seconds
            remaining = max(0, self.recovery_timeout - elapsed)
            return f"{remaining}s"
        return "N/A"
    
    def force_open(self):
        """Manually open circuit for testing"""
        self._change_state(CircuitState.OPEN)
        self.last_failure_time = datetime.now()
        print("⚡ Circuit manually OPENED")
    
    def reset(self):
        """Reset circuit breaker"""
        self._change_state(CircuitState.CLOSED)
        self.failure_count = 0
        self.success_count = 0
        print("🔄 Circuit RESET to CLOSED")
    
    def show_history(self):
        """Show state change history"""
        if not self.state_history:
            print("No state changes yet")
            return
        
        print("\n📜 State Change History:")
        for change in self.state_history[-5:]:  # Show last 5
            print(f"  {change['from']} → {change['to']} at {change['timestamp'].split('T')[1][:8]}")

# Setup
api_key = load_api_key()
if not api_key:
    print("❌ No API key found!")
    exit()

client = openai.OpenAI(api_key=api_key)
circuit_breaker = CircuitBreaker(client, failure_threshold=3, recovery_timeout=30)

print("⚡ Circuit Breaker Demo")
print("=" * 50)
print("Protects against cascading failures!")
print("Commands: 'status', 'history', 'force_open', 'reset', 'simulate', 'quit'")
print("-" * 50)

while True:
    user_input = input("\nYour message: ").strip()
    
    if user_input.lower() == 'quit':
        break
    
    elif user_input.lower() == 'status':
        status = circuit_breaker.get_status()
        print(f"\n📊 Circuit Breaker Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
        continue
    
    elif user_input.lower() == 'history':
        circuit_breaker.show_history()
        continue
    
    elif user_input.lower() == 'force_open':
        circuit_breaker.force_open()
        continue
    
    elif user_input.lower() == 'reset':
        circuit_breaker.reset()
        continue
    
    elif user_input.lower() == 'simulate':
        print("\n🧪 Simulating failure scenario...")
        
        # Temporarily use bad model to trigger failures
        original_client = circuit_breaker.client
        bad_client = openai.OpenAI(api_key="invalid_key")
        circuit_breaker.client = bad_client
        
        for i in range(5):
            print(f"\n📝 Request {i+1}/5:")
            messages = [{"role": "user", "content": "Test"}]
            response, error = circuit_breaker.call(messages)
            
            if response:
                print(f"Response: {response[:50]}...")
            else:
                print(f"Blocked/Failed: {error}")
            
            time.sleep(1)
        
        # Restore good client
        circuit_breaker.client = original_client
        print("\n✅ Restored good client - wait for recovery...")
        continue
    
    # Normal request
    messages = [{"role": "user", "content": user_input}]
    response, error = circuit_breaker.call(messages)
    
    if response:
        print(f"\n🤖 {response}")
    else:
        print(f"\n⚠️ {error}")
        
        if circuit_breaker.state == CircuitState.OPEN:
            print("💡 Circuit is OPEN - protecting against cascading failures")
            print(f"   Will attempt recovery in {circuit_breaker._time_to_recovery()}")

# Final stats
print("\n📊 Final Statistics:")
status = circuit_breaker.get_status()
for key, value in status.items():
    print(f"  {key}: {value}")

print("\n👋 Goodbye!")
