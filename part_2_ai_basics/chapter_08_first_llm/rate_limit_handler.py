# From: Zero to AI Agent, Chapter 8, Section 8.4
# File: rate_limit_handler.py

import openai
from pathlib import Path
import time
from datetime import datetime, timedelta

def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

class RateLimitHandler:
    """Handle rate limits intelligently"""
    
    def __init__(self, client):
        self.client = client
        self.request_times = []
        self.requests_per_minute = 20  # Conservative limit
        self.last_rate_limit_time = None
        
    def wait_if_needed(self):
        """Check if we need to wait before making a request"""
        now = datetime.now()
        
        # Clean old request times (older than 1 minute)
        one_minute_ago = now - timedelta(minutes=1)
        self.request_times = [t for t in self.request_times if t > one_minute_ago]
        
        # Check if we're approaching the limit
        if len(self.request_times) >= self.requests_per_minute:
            # Calculate how long to wait
            oldest_request = self.request_times[0]
            wait_until = oldest_request + timedelta(minutes=1)
            wait_seconds = (wait_until - now).total_seconds()
            
            if wait_seconds > 0:
                print(f"⏳ Approaching rate limit. Waiting {wait_seconds:.1f} seconds...")
                time.sleep(wait_seconds + 0.1)  # Add small buffer
    
    def make_request(self, messages):
        """Make a request with rate limit handling"""
        self.wait_if_needed()
        
        try:
            # Record request time
            self.request_times.append(datetime.now())
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            
            # Check response headers for rate limit info
            # Note: OpenAI Python client may not expose all headers
            
            return response.choices[0].message.content, None
            
        except openai.RateLimitError as e:
            self.last_rate_limit_time = datetime.now()
            
            # Parse retry-after if available
            retry_after = getattr(e, 'retry_after', None)
            if retry_after:
                print(f"⏳ Rate limited. Retry after {retry_after} seconds")
                time.sleep(retry_after)
            else:
                # Default wait
                print("⏳ Rate limited. Waiting 60 seconds...")
                time.sleep(60)
            
            # Try once more
            return self.make_request(messages)
            
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def get_status(self):
        """Get current rate limit status"""
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        recent_requests = len([t for t in self.request_times if t > one_minute_ago])
        
        return {
            'recent_requests': recent_requests,
            'limit': self.requests_per_minute,
            'available': self.requests_per_minute - recent_requests
        }

# Setup
api_key = load_api_key()
if not api_key:
    print("❌ No API key found!")
    exit()

client = openai.OpenAI(api_key=api_key)
rate_handler = RateLimitHandler(client)

print("🚦 Rate Limit Handler Demo")
print("=" * 50)
print(f"Rate limit: {rate_handler.requests_per_minute} requests/minute")
print("Commands: 'status', 'burst', 'quit'")
print("-" * 50)

while True:
    command = input("\nEnter command or message: ").strip()
    
    if command.lower() == 'quit':
        break
    
    elif command.lower() == 'status':
        status = rate_handler.get_status()
        print(f"\n📊 Rate Limit Status:")
        print(f"  Recent requests: {status['recent_requests']}")
        print(f"  Limit: {status['limit']}/minute")
        print(f"  Available: {status['available']}")
        continue
    
    elif command.lower() == 'burst':
        # Test rate limiting with burst requests
        print("\n🚀 Sending burst of requests...")
        for i in range(5):
            print(f"\nRequest {i+1}/5:")
            messages = [{"role": "user", "content": f"Say '{i+1}'"}]
            response, error = rate_handler.make_request(messages)
            
            if response:
                print(f"✅ Response: {response}")
            else:
                print(f"❌ Error: {error}")
            
            # Show status
            status = rate_handler.get_status()
            print(f"   [{status['recent_requests']}/{status['limit']} requests used]")
        continue
    
    # Normal message
    messages = [{"role": "user", "content": command}]
    response, error = rate_handler.make_request(messages)
    
    if response:
        print(f"\n🤖 Response: {response}")
        status = rate_handler.get_status()
        print(f"📊 Requests: {status['recent_requests']}/{status['limit']}")
    else:
        print(f"\n❌ {error}")

print("\n👋 Goodbye!")
