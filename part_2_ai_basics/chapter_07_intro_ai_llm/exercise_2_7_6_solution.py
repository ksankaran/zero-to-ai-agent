# From: Zero to AI Agent, Chapter 7, Section 7.6
# File: exercise_2_7_6_solution.py

"""
Exercise 2 Solution: Multi-Provider Authentication
A class that authenticates with multiple providers and automatically fails over.
"""

import os
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import time


# Load environment variables
load_dotenv()


class ProviderStatus(Enum):
    """Status of each provider"""
    AVAILABLE = "available"
    FAILED = "failed"
    RATE_LIMITED = "rate_limited"
    NOT_CONFIGURED = "not_configured"
    UNKNOWN = "unknown"


@dataclass
class ProviderInfo:
    """Information about a provider"""
    name: str
    status: ProviderStatus
    client: Optional[Any] = None
    last_error: Optional[str] = None
    last_check: Optional[datetime] = None
    priority: int = 0
    

class MultiProviderAuth:
    """
    Multi-provider authentication with automatic failover.
    Manages connections to multiple AI providers and switches between them seamlessly.
    """
    
    def __init__(self, preferred_order: List[str] = None):
        """
        Initialize multi-provider authentication
        
        Args:
            preferred_order: List of providers in order of preference
                           Default: ["openai", "anthropic", "google"]
        """
        self.providers = {}
        self.preferred_order = preferred_order or ["openai", "anthropic", "google"]
        self.current_provider = None
        self.fallback_chain = []
        
        # Initialize all providers
        self._initialize_providers()
        
        # Set up fallback chain
        self._setup_fallback_chain()
    
    def _initialize_providers(self):
        """Initialize all available providers"""
        
        # OpenAI
        self._init_openai()
        
        # Anthropic
        self._init_anthropic()
        
        # Google Gemini
        self._init_google()
        
        print(f"✅ Initialized {len(self.providers)} providers")
    
    def _init_openai(self):
        """Initialize OpenAI provider"""
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key or api_key == "ADD_YOUR_KEY_HERE":
            self.providers["openai"] = ProviderInfo(
                name="openai",
                status=ProviderStatus.NOT_CONFIGURED,
                priority=self.preferred_order.index("openai") if "openai" in self.preferred_order else 99
            )
            return
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            
            # Test the connection
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            
            self.providers["openai"] = ProviderInfo(
                name="openai",
                status=ProviderStatus.AVAILABLE,
                client=client,
                last_check=datetime.now(),
                priority=self.preferred_order.index("openai") if "openai" in self.preferred_order else 99
            )
            print("✅ OpenAI authenticated successfully")
            
        except ImportError:
            self.providers["openai"] = ProviderInfo(
                name="openai",
                status=ProviderStatus.FAILED,
                last_error="Package not installed",
                priority=99
            )
        except Exception as e:
            self.providers["openai"] = ProviderInfo(
                name="openai",
                status=ProviderStatus.FAILED,
                last_error=str(e)[:100],
                last_check=datetime.now(),
                priority=self.preferred_order.index("openai") if "openai" in self.preferred_order else 99
            )
    
    def _init_anthropic(self):
        """Initialize Anthropic provider"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not api_key or api_key == "ADD_YOUR_KEY_HERE":
            self.providers["anthropic"] = ProviderInfo(
                name="anthropic",
                status=ProviderStatus.NOT_CONFIGURED,
                priority=self.preferred_order.index("anthropic") if "anthropic" in self.preferred_order else 99
            )
            return
        
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=api_key)
            
            # Test the connection
            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1,
                messages=[{"role": "user", "content": "test"}]
            )
            
            self.providers["anthropic"] = ProviderInfo(
                name="anthropic",
                status=ProviderStatus.AVAILABLE,
                client=client,
                last_check=datetime.now(),
                priority=self.preferred_order.index("anthropic") if "anthropic" in self.preferred_order else 99
            )
            print("✅ Anthropic authenticated successfully")
            
        except ImportError:
            self.providers["anthropic"] = ProviderInfo(
                name="anthropic",
                status=ProviderStatus.FAILED,
                last_error="Package not installed",
                priority=99
            )
        except Exception as e:
            self.providers["anthropic"] = ProviderInfo(
                name="anthropic",
                status=ProviderStatus.FAILED,
                last_error=str(e)[:100],
                last_check=datetime.now(),
                priority=self.preferred_order.index("anthropic") if "anthropic" in self.preferred_order else 99
            )
    
    def _init_google(self):
        """Initialize Google Gemini provider"""
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        
        if not api_key or api_key == "ADD_YOUR_KEY_HERE":
            self.providers["google"] = ProviderInfo(
                name="google",
                status=ProviderStatus.NOT_CONFIGURED,
                priority=self.preferred_order.index("google") if "google" in self.preferred_order else 99
            )
            return
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            
            # Test the connection
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("test")
            
            self.providers["google"] = ProviderInfo(
                name="google",
                status=ProviderStatus.AVAILABLE,
                client=genai,
                last_check=datetime.now(),
                priority=self.preferred_order.index("google") if "google" in self.preferred_order else 99
            )
            print("✅ Google Gemini authenticated successfully")
            
        except ImportError:
            self.providers["google"] = ProviderInfo(
                name="google",
                status=ProviderStatus.FAILED,
                last_error="Package not installed",
                priority=99
            )
        except Exception as e:
            self.providers["google"] = ProviderInfo(
                name="google",
                status=ProviderStatus.FAILED,
                last_error=str(e)[:100],
                last_check=datetime.now(),
                priority=self.preferred_order.index("google") if "google" in self.preferred_order else 99
            )
    
    def _setup_fallback_chain(self):
        """Set up the fallback chain based on availability and preference"""
        # Sort providers by priority and availability
        available_providers = [
            p for p in self.providers.values()
            if p.status == ProviderStatus.AVAILABLE
        ]
        
        # Sort by priority
        available_providers.sort(key=lambda p: p.priority)
        
        self.fallback_chain = [p.name for p in available_providers]
        
        if self.fallback_chain:
            self.current_provider = self.fallback_chain[0]
            print(f"📍 Primary provider: {self.current_provider}")
            if len(self.fallback_chain) > 1:
                print(f"🔄 Fallback chain: {' -> '.join(self.fallback_chain)}")
        else:
            print("⚠️ No available providers!")
    
    def get_client(self, provider: str = None) -> Optional[Any]:
        """
        Get client for a specific provider or current provider
        
        Args:
            provider: Name of provider, or None for current provider
        
        Returns:
            Client object or None if not available
        """
        if provider is None:
            provider = self.current_provider
        
        if provider and provider in self.providers:
            provider_info = self.providers[provider]
            if provider_info.status == ProviderStatus.AVAILABLE:
                return provider_info.client
        
        return None
    
    def failover_to_next(self) -> bool:
        """
        Switch to the next available provider in the fallback chain
        
        Returns:
            True if failover successful, False if no more providers
        """
        if not self.current_provider or not self.fallback_chain:
            return False
        
        try:
            current_index = self.fallback_chain.index(self.current_provider)
            if current_index < len(self.fallback_chain) - 1:
                self.current_provider = self.fallback_chain[current_index + 1]
                print(f"🔄 Failed over to: {self.current_provider}")
                return True
        except ValueError:
            pass
        
        print("❌ No more providers to fail over to")
        return False
    
    def mark_provider_failed(self, provider: str, error: str):
        """Mark a provider as failed and trigger failover"""
        if provider in self.providers:
            self.providers[provider].status = ProviderStatus.FAILED
            self.providers[provider].last_error = error
            self.providers[provider].last_check = datetime.now()
            
            # Remove from fallback chain
            if provider in self.fallback_chain:
                self.fallback_chain.remove(provider)
            
            # Failover if this was the current provider
            if provider == self.current_provider:
                self.failover_to_next()
    
    def mark_provider_rate_limited(self, provider: str, retry_after: int = 60):
        """Mark a provider as rate limited and schedule retry"""
        if provider in self.providers:
            self.providers[provider].status = ProviderStatus.RATE_LIMITED
            self.providers[provider].last_error = f"Rate limited. Retry after {retry_after}s"
            self.providers[provider].last_check = datetime.now()
            
            print(f"⏳ {provider} rate limited. Will retry in {retry_after}s")
            
            # Temporarily remove from fallback chain
            if provider in self.fallback_chain:
                self.fallback_chain.remove(provider)
            
            # Failover if this was the current provider
            if provider == self.current_provider:
                self.failover_to_next()
    
    def make_request(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """
        Make a request with automatic failover
        
        Args:
            prompt: The prompt to send
            max_retries: Maximum number of providers to try
        
        Returns:
            Response text or None if all providers failed
        """
        attempts = 0
        original_provider = self.current_provider
        
        while attempts < max_retries and self.current_provider:
            provider_name = self.current_provider
            provider = self.providers.get(provider_name)
            
            if not provider or provider.status != ProviderStatus.AVAILABLE:
                if not self.failover_to_next():
                    break
                continue
            
            try:
                print(f"🔄 Attempting with {provider_name}...")
                
                # Make provider-specific request
                if provider_name == "openai":
                    response = self._request_openai(provider.client, prompt)
                elif provider_name == "anthropic":
                    response = self._request_anthropic(provider.client, prompt)
                elif provider_name == "google":
                    response = self._request_google(provider.client, prompt)
                else:
                    raise ValueError(f"Unknown provider: {provider_name}")
                
                print(f"✅ Success with {provider_name}")
                return response
                
            except Exception as e:
                error_str = str(e).lower()
                
                # Check if rate limited
                if "rate" in error_str and "limit" in error_str:
                    self.mark_provider_rate_limited(provider_name)
                else:
                    self.mark_provider_failed(provider_name, str(e)[:100])
                
                print(f"❌ {provider_name} failed: {str(e)[:50]}")
                attempts += 1
                
                # Try failover
                if not self.failover_to_next():
                    break
        
        print(f"❌ All providers failed after {attempts} attempts")
        return None
    
    def _request_openai(self, client, prompt: str) -> str:
        """Make request to OpenAI"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        return response.choices[0].message.content
    
    def _request_anthropic(self, client, prompt: str) -> str:
        """Make request to Anthropic"""
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    
    def _request_google(self, client, prompt: str) -> str:
        """Make request to Google Gemini"""
        model = client.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of all providers"""
        return {
            "current_provider": self.current_provider,
            "fallback_chain": self.fallback_chain,
            "providers": {
                name: {
                    "status": p.status.value,
                    "last_error": p.last_error,
                    "last_check": p.last_check.isoformat() if p.last_check else None,
                    "priority": p.priority
                }
                for name, p in self.providers.items()
            }
        }
    
    def display_status(self):
        """Display current status of all providers"""
        print("=" * 60)
        print("🔌 Multi-Provider Authentication Status")
        print("=" * 60)
        
        status = self.get_status()
        
        print(f"\n📍 Current Provider: {status['current_provider'] or 'None'}")
        
        if status['fallback_chain']:
            print(f"🔄 Fallback Chain: {' -> '.join(status['fallback_chain'])}")
        
        print("\n📊 Provider Status:")
        for name, info in status['providers'].items():
            status_icon = {
                "available": "✅",
                "failed": "❌",
                "rate_limited": "⏳",
                "not_configured": "⚫",
                "unknown": "❓"
            }.get(info['status'], "❓")
            
            print(f"  {status_icon} {name}: {info['status']}")
            if info['last_error']:
                print(f"      Error: {info['last_error']}")


# Demo and testing
if __name__ == "__main__":
    print("Multi-Provider Authentication Demo")
    print("=" * 60)
    
    # Create multi-provider auth with custom preference order
    auth = MultiProviderAuth(preferred_order=["google", "openai", "anthropic"])
    
    # Display initial status
    auth.display_status()
    
    # Test making requests with failover
    print("\n" + "=" * 60)
    print("Testing Requests with Automatic Failover")
    print("=" * 60)
    
    test_prompts = [
        "Say 'Hello from AI!'",
        "What is 2+2?",
        "Complete: The sky is..."
    ]
    
    for prompt in test_prompts:
        print(f"\n📝 Prompt: {prompt}")
        response = auth.make_request(prompt)
        if response:
            print(f"📬 Response: {response[:100]}")
        else:
            print("❌ No response (all providers failed)")
    
    # Final status
    print("\n")
    auth.display_status()
