# From: Zero to AI Agent, Chapter 8, Section 8.4
# File: exercise_2_8_4_resilient_caller.py

import openai
from pathlib import Path
import time

def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

class ResilientCaller:
    """Adaptive API caller that adjusts to errors"""
    
    def __init__(self, client):
        self.client = client
        self.models = ["gpt-3.5-turbo", "gpt-3.5-turbo-0125"]  # Fallback models
        self.health_score = 100  # 0-100, starts healthy
        self.error_count = 0
        self.success_count = 0
        self.current_model_index = 0
        self.error_history = []
    
    def update_health(self, success, error_type=None):
        """Update health score based on success/failure"""
        if success:
            self.success_count += 1
            # Slowly recover health
            self.health_score = min(100, self.health_score + 5)
        else:
            self.error_count += 1
            # Different errors affect health differently
            if error_type == 'RateLimitError':
                self.health_score = max(0, self.health_score - 30)
            elif error_type == 'APITimeoutError':
                self.health_score = max(0, self.health_score - 15)
            else:
                self.health_score = max(0, self.health_score - 20)
            
            self.error_history.append(error_type)
            # Keep only last 10 errors
            self.error_history = self.error_history[-10:]
    
    def get_adjusted_params(self):
        """Adjust parameters based on health"""
        if self.health_score > 80:
            # Healthy - normal operation
            return {
                'max_tokens': None,
                'temperature': 0.7,
                'timeout': 30
            }
        elif self.health_score > 50:
            # Degraded - be conservative
            return {
                'max_tokens': 100,
                'temperature': 0.5,
                'timeout': 20
            }
        else:
            # Unhealthy - minimal requests
            return {
                'max_tokens': 50,
                'temperature': 0.3,
                'timeout': 10
            }
    
    def make_resilient_call(self, messages):
        """Make API call with fallback strategies"""
        params = self.get_adjusted_params()
        
        # Try current model
        for model_offset in range(len(self.models)):
            model_index = (self.current_model_index + model_offset) % len(self.models)
            model = self.models[model_index]
            
            print(f"🔧 Trying {model} (Health: {self.health_score}%)")
            
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=params['max_tokens'],
                    temperature=params['temperature'],
                    timeout=params['timeout']
                )
                
                # Success!
                self.update_health(True)
                
                # If we had to fallback, remember the working model
                if model_offset > 0:
                    self.current_model_index = model_index
                    print(f"✅ Switched to {model} as primary")
                
                return response.choices[0].message.content, None
                
            except openai.RateLimitError as e:
                print(f"⏳ Rate limit on {model}")
                self.update_health(False, 'RateLimitError')
                
                if self.health_score < 30:
                    print("🛑 Health critical - waiting 30 seconds")
                    time.sleep(30)
                else:
                    time.sleep(5)
                    
            except openai.BadRequestError as e:
                print(f"❌ Bad request on {model}")
                self.update_health(False, 'BadRequestError')
                
                # Try simpler message
                if len(messages[-1]['content']) > 100:
                    print("📝 Trying with shorter message...")
                    short_messages = [
                        {"role": "user", "content": messages[-1]['content'][:100]}
                    ]
                    return self.make_resilient_call(short_messages)
            
            except openai.APITimeoutError as e:
                print(f"⏱️ Timeout on {model}")
                self.update_health(False, 'APITimeoutError')
                time.sleep(2)
                    
            except Exception as e:
                print(f"❌ Error with {model}: {type(e).__name__}")
                self.update_health(False, type(e).__name__)
        
        # All attempts failed
        return None, "All fallback strategies exhausted"
    
    def get_status(self):
        """Get current health status"""
        status = "🟢 Healthy" if self.health_score > 80 else \
                 "🟡 Degraded" if self.health_score > 50 else \
                 "🔴 Critical"
        
        # Analyze error patterns
        recommendations = []
        if self.error_history.count('RateLimitError') > 3:
            recommendations.append("Implement request throttling")
        if self.error_history.count('APITimeoutError') > 2:
            recommendations.append("Check network connection")
        
        return {
            'status': status,
            'health': self.health_score,
            'errors': self.error_count,
            'successes': self.success_count,
            'model': self.models[self.current_model_index],
            'recommendations': recommendations
        }

# Setup
api_key = load_api_key()
if not api_key:
    print("❌ No API key found!")
    exit()

client = openai.OpenAI(api_key=api_key)
resilient = ResilientCaller(client)

print("💪 Resilient API Caller")
print("=" * 50)
print("Automatically adapts to errors!")
print("Commands: 'status', 'stress_test', 'quit'")
print("-" * 50)

while True:
    user_input = input("\nYour message: ").strip()
    
    if user_input.lower() == 'quit':
        break
    
    elif user_input.lower() == 'status':
        status = resilient.get_status()
        print(f"\n📊 System Status:")
        print(f"  Status: {status['status']}")
        print(f"  Health: {status['health']}%")
        print(f"  Errors: {status['errors']}")
        print(f"  Successes: {status['successes']}")
        print(f"  Current Model: {status['model']}")
        if status['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in status['recommendations']:
                print(f"  • {rec}")
        continue
    
    elif user_input.lower() == 'stress_test':
        print("\n🧪 Stress testing resilience...")
        
        test_messages = [
            "Hello",
            "Write a very long essay about everything in the universe",  # Might hit limits
            "What's 2+2?",
            "⚡" * 1000,  # Weird input
            "Normal question about Python"
        ]
        
        for msg in test_messages:
            print(f"\n📝 Testing: '{msg[:30]}...'")
            messages = [{"role": "user", "content": msg}]
            response, error = resilient.make_resilient_call(messages)
            
            if response:
                print(f"✅ Got response: {response[:50]}...")
            else:
                print(f"❌ Failed: {error}")
            
            # Show health after each
            print(f"   Health: {resilient.health_score}%")
        
        continue
    
    # Normal request
    messages = [{"role": "user", "content": user_input}]
    response, error = resilient.make_resilient_call(messages)
    
    if response:
        print(f"\n🤖 {response}")
    else:
        print(f"\n❌ {error}")
    
    # Always show health
    status = resilient.get_status()
    print(f"\n[{status['status']} - Health: {status['health']}%]")

print("\n📊 Final Statistics:")
status = resilient.get_status()
for key, value in status.items():
    if key != 'recommendations':
        print(f"  {key}: {value}")
print("\n👋 Goodbye!")
