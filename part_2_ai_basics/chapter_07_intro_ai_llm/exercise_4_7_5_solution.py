# From: Zero to AI Agent, Chapter 7, Section 7.5
# File: exercise_4_7_5_solution.py

"""
Exercise 4 Solution: API Abstraction
Write a wrapper class that works with multiple LLM providers.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod
import json
import time
from enum import Enum


class Provider(Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    COHERE = "cohere"
    HUGGINGFACE = "huggingface"


@dataclass
class LLMResponse:
    """Unified response format."""
    text: str
    provider: str
    model: str
    tokens_used: int
    cost: float
    latency: float
    metadata: Dict[str, Any]


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate completion."""
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict], **kwargs) -> LLMResponse:
        """Chat completion."""
        pass
    
    @abstractmethod
    def estimate_tokens(self, text: str) -> int:
        """Estimate token count."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available."""
        pass


class OpenAIProvider(BaseLLMProvider):
    """OpenAI provider implementation."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.pricing = {
            "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03}
        }
        
        # Import OpenAI library
        try:
            import openai
            self.client = openai.OpenAI(api_key=api_key)
            self.available = True
        except ImportError:
            print("OpenAI library not installed. Run: pip install openai")
            self.available = False
        except Exception as e:
            print(f"OpenAI initialization error: {e}")
            self.available = False
    
    def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """OpenAI completion."""
        return self.chat([{"role": "user", "content": prompt}], **kwargs)
    
    def chat(self, messages: List[Dict], **kwargs) -> LLMResponse:
        """OpenAI chat completion."""
        if not self.available:
            raise Exception("OpenAI provider not available")
        
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=kwargs.get("model", self.model),
                messages=messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 512),
                top_p=kwargs.get("top_p", 1.0),
                frequency_penalty=kwargs.get("frequency_penalty", 0),
                presence_penalty=kwargs.get("presence_penalty", 0)
            )
            
            latency = time.time() - start_time
            
            # Calculate cost
            model = kwargs.get("model", self.model)
            if model in self.pricing:
                input_cost = (response.usage.prompt_tokens / 1000) * \
                           self.pricing[model]["input"]
                output_cost = (response.usage.completion_tokens / 1000) * \
                            self.pricing[model]["output"]
                total_cost = input_cost + output_cost
            else:
                total_cost = 0
            
            return LLMResponse(
                text=response.choices[0].message.content,
                provider="OpenAI",
                model=model,
                tokens_used=response.usage.total_tokens,
                cost=total_cost,
                latency=latency,
                metadata={
                    "finish_reason": response.choices[0].finish_reason,
                    "response_id": response.id
                }
            )
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {e}")
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate tokens for OpenAI."""
        # Rough estimation: 1 token ≈ 4 characters
        return len(text) // 4
    
    def is_available(self) -> bool:
        """Check availability."""
        return self.available


class AnthropicProvider(BaseLLMProvider):
    """Anthropic provider implementation."""
    
    def __init__(self, api_key: str, model: str = "claude-3-haiku-20240307"):
        self.api_key = api_key
        self.model = model
        self.pricing = {
            "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
            "claude-3-sonnet": {"input": 0.003, "output": 0.015},
            "claude-3-opus": {"input": 0.015, "output": 0.075}
        }
        
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
            self.available = True
        except ImportError:
            print("Anthropic library not installed. Run: pip install anthropic")
            self.available = False
        except Exception as e:
            print(f"Anthropic initialization error: {e}")
            self.available = False
    
    def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """Anthropic completion."""
        return self.chat([{"role": "user", "content": prompt}], **kwargs)
    
    def chat(self, messages: List[Dict], **kwargs) -> LLMResponse:
        """Anthropic chat completion."""
        if not self.available:
            raise Exception("Anthropic provider not available")
        
        start_time = time.time()
        
        try:
            # Convert messages format if needed
            if messages[0].get("role") == "system":
                system = messages[0]["content"]
                messages = messages[1:]
            else:
                system = None
            
            response = self.client.messages.create(
                model=kwargs.get("model", self.model),
                messages=messages,
                max_tokens=kwargs.get("max_tokens", 512),
                temperature=kwargs.get("temperature", 0.7),
                system=system
            )
            
            latency = time.time() - start_time
            
            # Estimate cost (simplified)
            tokens_used = len(prompt) // 4 + len(response.content[0].text) // 4
            cost = (tokens_used / 1000) * 0.001  # Simplified pricing
            
            return LLMResponse(
                text=response.content[0].text,
                provider="Anthropic",
                model=kwargs.get("model", self.model),
                tokens_used=tokens_used,
                cost=cost,
                latency=latency,
                metadata={
                    "response_id": response.id,
                    "stop_reason": response.stop_reason
                }
            )
            
        except Exception as e:
            raise Exception(f"Anthropic API error: {e}")
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate tokens for Anthropic."""
        return len(text) // 4
    
    def is_available(self) -> bool:
        """Check availability."""
        return self.available


class UnifiedLLM:
    """
    Unified LLM interface that works with multiple providers.
    Easy switching, fallback support, and unified response format.
    """
    
    def __init__(self):
        self.providers: Dict[Provider, BaseLLMProvider] = {}
        self.primary_provider: Optional[Provider] = None
        self.fallback_chain: List[Provider] = []
        self.usage_stats: Dict[str, Any] = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_cost": 0.0,
            "provider_usage": {},
            "errors": []
        }
    
    def add_provider(self, provider: Provider, config: Dict) -> None:
        """Add a provider with configuration."""
        
        if provider == Provider.OPENAI:
            self.providers[provider] = OpenAIProvider(
                api_key=config["api_key"],
                model=config.get("model", "gpt-3.5-turbo")
            )
        elif provider == Provider.ANTHROPIC:
            self.providers[provider] = AnthropicProvider(
                api_key=config["api_key"],
                model=config.get("model", "claude-3-haiku-20240307")
            )
        # Add more providers as needed
        
        # Set as primary if first provider
        if self.primary_provider is None and \
           self.providers[provider].is_available():
            self.primary_provider = provider
        
        # Add to fallback chain
        if provider not in self.fallback_chain and \
           self.providers[provider].is_available():
            self.fallback_chain.append(provider)
    
    def set_primary(self, provider: Provider) -> None:
        """Set primary provider."""
        if provider in self.providers and \
           self.providers[provider].is_available():
            self.primary_provider = provider
        else:
            raise ValueError(f"Provider {provider} not available")
    
    def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """
        Generate completion with automatic fallback.
        
        Args:
            prompt: Input prompt
            **kwargs: Additional parameters
            
        Returns:
            LLMResponse with unified format
        """
        
        self.usage_stats["total_requests"] += 1
        
        # Try primary provider first
        if self.primary_provider:
            try:
                response = self.providers[self.primary_provider].complete(
                    prompt, **kwargs
                )
                self._update_stats(response)
                return response
            except Exception as e:
                self.usage_stats["errors"].append({
                    "provider": self.primary_provider.value,
                    "error": str(e),
                    "timestamp": time.time()
                })
        
        # Try fallback providers
        for provider in self.fallback_chain:
            if provider == self.primary_provider:
                continue  # Already tried
            
            try:
                response = self.providers[provider].complete(prompt, **kwargs)
                self._update_stats(response)
                print(f"⚠️ Used fallback provider: {provider.value}")
                return response
            except Exception as e:
                self.usage_stats["errors"].append({
                    "provider": provider.value,
                    "error": str(e),
                    "timestamp": time.time()
                })
                continue
        
        raise Exception("All providers failed")
    
    def chat(self, messages: List[Dict], **kwargs) -> LLMResponse:
        """Chat completion with automatic fallback."""
        
        self.usage_stats["total_requests"] += 1
        
        # Try primary provider
        if self.primary_provider:
            try:
                response = self.providers[self.primary_provider].chat(
                    messages, **kwargs
                )
                self._update_stats(response)
                return response
            except Exception as e:
                self.usage_stats["errors"].append({
                    "provider": self.primary_provider.value,
                    "error": str(e),
                    "timestamp": time.time()
                })
        
        # Try fallbacks
        for provider in self.fallback_chain:
            if provider == self.primary_provider:
                continue
            
            try:
                response = self.providers[provider].chat(messages, **kwargs)
                self._update_stats(response)
                print(f"⚠️ Used fallback provider: {provider.value}")
                return response
            except Exception as e:
                continue
        
        raise Exception("All providers failed")
    
    def _update_stats(self, response: LLMResponse):
        """Update usage statistics."""
        self.usage_stats["total_tokens"] += response.tokens_used
        self.usage_stats["total_cost"] += response.cost
        
        if response.provider not in self.usage_stats["provider_usage"]:
            self.usage_stats["provider_usage"][response.provider] = {
                "requests": 0,
                "tokens": 0,
                "cost": 0.0,
                "avg_latency": 0.0
            }
        
        stats = self.usage_stats["provider_usage"][response.provider]
        stats["requests"] += 1
        stats["tokens"] += response.tokens_used
        stats["cost"] += response.cost
        
        # Update average latency
        prev_avg = stats["avg_latency"]
        stats["avg_latency"] = (prev_avg * (stats["requests"] - 1) + 
                                response.latency) / stats["requests"]
    
    def get_stats(self) -> Dict:
        """Get usage statistics."""
        return self.usage_stats
    
    def estimate_cost(self, prompt: str, provider: Optional[Provider] = None) -> float:
        """Estimate cost before making request."""
        
        if provider is None:
            provider = self.primary_provider
        
        if provider and provider in self.providers:
            tokens = self.providers[provider].estimate_tokens(prompt)
            # Simplified cost estimation
            return (tokens / 1000) * 0.002  # Average cost
        
        return 0.0
    
    def compare_providers(self, prompt: str) -> Dict[str, LLMResponse]:
        """Compare response from all available providers."""
        
        results = {}
        
        for provider, llm in self.providers.items():
            if llm.is_available():
                try:
                    response = llm.complete(prompt)
                    results[provider.value] = response
                except Exception as e:
                    results[provider.value] = f"Error: {e}"
        
        return results


def demonstrate_usage():
    """Demonstrate the unified LLM interface."""
    
    print("=" * 70)
    print("UNIFIED LLM INTERFACE DEMONSTRATION")
    print("=" * 70)
    
    # Example usage code
    usage_code = '''
# Initialize unified interface
llm = UnifiedLLM()

# Add multiple providers
llm.add_provider(Provider.OPENAI, {
    "api_key": os.getenv("OPENAI_API_KEY"),
    "model": "gpt-3.5-turbo"
})

llm.add_provider(Provider.ANTHROPIC, {
    "api_key": os.getenv("ANTHROPIC_API_KEY"),
    "model": "claude-3-haiku-20240307"
})

# Set primary provider
llm.set_primary(Provider.OPENAI)

# Simple completion - automatically handles fallback!
response = llm.complete(
    "Explain machine learning in one sentence",
    temperature=0.5,
    max_tokens=100
)

print(f"Response: {response.text}")
print(f"Provider: {response.provider}")
print(f"Cost: ${response.cost:.6f}")
print(f"Latency: {response.latency:.2f}s")

# Chat completion
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What is Python?"}
]

response = llm.chat(messages)

# Compare providers
comparison = llm.compare_providers("What is 2+2?")
for provider, result in comparison.items():
    if isinstance(result, LLMResponse):
        print(f"{provider}: {result.text}")

# Get usage statistics
stats = llm.get_stats()
print(f"Total requests: {stats['total_requests']}")
print(f"Total cost: ${stats['total_cost']:.4f}")

# Estimate cost before making request
estimated_cost = llm.estimate_cost("Long prompt here..." * 100)
print(f"Estimated cost: ${estimated_cost:.6f}")
    '''
    
    print("USAGE EXAMPLE:")
    print(usage_code)
    
    # Show migration simplicity
    print("\n" + "=" * 70)
    print("MIGRATION SIMPLICITY")
    print("=" * 70)
    
    migration_example = '''
# Switching providers is ONE LINE!

# Before migration (using OpenAI)
llm.set_primary(Provider.OPENAI)
response = llm.complete("Hello world")

# After migration (using Anthropic)
llm.set_primary(Provider.ANTHROPIC)
response = llm.complete("Hello world")  # Same code!

# Or gradually migrate with weighted selection
import random

def gradual_migration(prompt: str, anthropic_weight: float = 0.1):
    """Gradually increase Anthropic usage."""
    if random.random() < anthropic_weight:
        llm.set_primary(Provider.ANTHROPIC)
    else:
        llm.set_primary(Provider.OPENAI)
    
    return llm.complete(prompt)

# Start with 10% on Anthropic, increase over time
response = gradual_migration("Test prompt", anthropic_weight=0.1)
    '''
    
    print(migration_example)


def main():
    """Run API abstraction exercise."""
    
    print("=" * 70)
    print("EXERCISE 4: API ABSTRACTION LAYER")
    print("=" * 70)
    
    # Note about the implementation
    print("\n📝 IMPLEMENTATION OVERVIEW:")
    print("-" * 50)
    print("This solution provides:")
    print("• Unified interface for multiple providers")
    print("• Automatic fallback on failures")
    print("• Consistent response format")
    print("• Usage tracking and statistics")
    print("• Cost estimation and tracking")
    print("• Easy provider switching")
    print("• Gradual migration support")
    
    # Show the usage
    demonstrate_usage()
    
    print("\n" + "=" * 70)
    print("KEY BENEFITS")
    print("=" * 70)
    
    benefits = [
        "✅ Provider Independence: Switch providers with one line",
        "✅ Reliability: Automatic fallback prevents downtime",
        "✅ Cost Control: Track and estimate costs across providers",
        "✅ Easy Migration: Gradually shift traffic between providers",
        "✅ Unified Interface: Same code regardless of provider",
        "✅ Statistics: Built-in usage and performance tracking",
        "✅ Extensible: Easy to add new providers"
    ]
    
    for benefit in benefits:
        print(benefit)
    
    print("\n" + "=" * 70)
    print("EXERCISE 4 COMPLETE")
    print("=" * 70)
    print("\n✅ You now have a production-ready multi-provider LLM interface!")
    print("   This abstraction layer makes provider switching trivial!")


if __name__ == "__main__":
    main()
