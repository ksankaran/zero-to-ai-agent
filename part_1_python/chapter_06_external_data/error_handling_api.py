# From: Zero to AI Agent, Chapter 6, Section 6.3
# File: 06_error_handling.py


import requests
import time
import json

print("🛡️ HANDLING API ERRORS GRACEFULLY\n")

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.retry_count = 3
        self.retry_delay = 2  # seconds
    
    def safe_request(self, url, method="GET", **kwargs):
        """Make a safe API request with error handling"""
        
        for attempt in range(self.retry_count):
            try:
                print(f"\n🔄 Attempt {attempt + 1}/{self.retry_count}")
                
                # Make the request
                if method == "GET":
                    response = self.session.get(url, timeout=10, **kwargs)
                elif method == "POST":
                    response = self.session.post(url, timeout=10, **kwargs)
                else:
                    response = self.session.request(method, url, timeout=10, **kwargs)
                
                # Check status code
                if response.status_code == 200:
                    print("✅ Success!")
                    return response.json()
                
                elif response.status_code == 429:
                    # Rate limited - wait and retry
                    retry_after = response.headers.get('Retry-After', self.retry_delay)
                    print(f"⏳ Rate limited. Waiting {retry_after} seconds...")
                    time.sleep(int(retry_after))
                    continue
                
                elif response.status_code == 401:
                    print("🔑 Authentication failed - check your API key")
                    return None
                
                elif response.status_code == 404:
                    print("❌ Not found - check the URL")
                    return None
                
                elif 500 <= response.status_code < 600:
                    print(f"🔥 Server error ({response.status_code}). Retrying...")
                    time.sleep(self.retry_delay)
                    continue
                
                else:
                    print(f"⚠️  Unexpected status: {response.status_code}")
                    return None
                    
            except requests.exceptions.Timeout:
                print("⏱️  Request timed out")
                if attempt < self.retry_count - 1:
                    print(f"Waiting {self.retry_delay} seconds before retry...")
                    time.sleep(self.retry_delay)
                    
            except requests.exceptions.ConnectionError:
                print("🌐 Connection error - check your internet")
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay)
                    
            except json.JSONDecodeError:
                print("📄 Invalid JSON response")
                return None
                
            except Exception as e:
                print(f"😱 Unexpected error: {e}")
                return None
        
        print("\n❌ All attempts failed")
        return None

# Demonstrate different error scenarios
client = APIClient()

print("="*50)
print("TESTING ERROR SCENARIOS:")
print("="*50)

# Scenario 1: Good request
print("\n1️⃣ GOOD REQUEST:")
data = client.safe_request("https://httpbin.org/get")
if data:
    print(f"   Received data: {list(data.keys())}")

# Scenario 2: 404 Not Found
print("\n2️⃣ NOT FOUND (404):")
data = client.safe_request("https://httpbin.org/status/404")

# Scenario 3: Server error (will retry)
print("\n3️⃣ SERVER ERROR (500):")
data = client.safe_request("https://httpbin.org/status/500")

# Scenario 4: Invalid domain
print("\n4️⃣ INVALID DOMAIN:")
data = client.safe_request("https://this-definitely-does-not-exist-12345.com")
