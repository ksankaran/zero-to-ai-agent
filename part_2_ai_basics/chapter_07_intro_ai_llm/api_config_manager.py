# From: Zero to AI Agent, Chapter 7, Section 7.6
# File: api_config_manager.py

"""
Centralized API configuration manager for working with multiple AI providers.
Handles loading, validation, and organization of API keys.
"""

import os
from dataclasses import dataclass
from typing import Optional, List, Dict
from dotenv import load_dotenv
import json


@dataclass
class APIConfig:
    """Centralized API configuration for multiple providers"""
    openai_key: Optional[str] = None
    anthropic_key: Optional[str] = None
    google_key: Optional[str] = None
    replicate_key: Optional[str] = None
    
    @classmethod
    def from_env(cls):
        """Load all API keys from environment variables"""
        # Try to load .env file first
        load_dotenv()
        
        return cls(
            openai_key=os.getenv("OPENAI_API_KEY"),
            anthropic_key=os.getenv("ANTHROPIC_API_KEY"),
            google_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"),
            replicate_key=os.getenv("REPLICATE_API_TOKEN")
        )
    
    @classmethod
    def from_json(cls, filepath: str = "config.json"):
        """Load API keys from a JSON configuration file"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(
                f"{filepath} not found! Copy config.example.json and add your keys"
            )
        
        with open(filepath) as f:
            config_data = json.load(f)
        
        return cls(
            openai_key=config_data.get("openai_key"),
            anthropic_key=config_data.get("anthropic_key"),
            google_key=config_data.get("google_key"),
            replicate_key=config_data.get("replicate_key")
        )
    
    def get_available_providers(self) -> List[str]:
        """Return list of providers with valid keys"""
        providers = []
        
        if self.openai_key and self.openai_key != "ADD_YOUR_KEY_HERE":
            providers.append("openai")
        if self.anthropic_key and self.anthropic_key != "ADD_YOUR_KEY_HERE":
            providers.append("anthropic")
        if self.google_key and self.google_key != "ADD_YOUR_KEY_HERE":
            providers.append("google")
        if self.replicate_key and self.replicate_key != "ADD_YOUR_KEY_HERE":
            providers.append("replicate")
        
        return providers
    
    def validate(self) -> bool:
        """Check if at least one key is configured properly"""
        available = self.get_available_providers()
        
        if not available:
            print("❌ No valid API keys found!")
            print("\nPlease configure at least one:")
            print("  - OPENAI_API_KEY")
            print("  - ANTHROPIC_API_KEY")
            print("  - GOOGLE_API_KEY")
            print("  - REPLICATE_API_TOKEN")
            return False
        
        print(f"✅ API keys loaded for: {', '.join(available)}")
        return True
    
    def get_primary_provider(self) -> Optional[str]:
        """Get the first available provider (useful for fallback)"""
        providers = self.get_available_providers()
        return providers[0] if providers else None
    
    def mask_key(self, key: str) -> str:
        """Safely display a masked version of an API key"""
        if not key:
            return "Not configured"
        if len(key) < 10:
            return "Invalid key"
        return f"{key[:7]}...{key[-4:]}"
    
    def display_status(self):
        """Display the status of all API keys"""
        print("=" * 60)
        print("API KEY CONFIGURATION STATUS")
        print("=" * 60)
        
        providers = {
            "OpenAI": self.openai_key,
            "Anthropic": self.anthropic_key,
            "Google": self.google_key,
            "Replicate": self.replicate_key
        }
        
        for name, key in providers.items():
            if key and key != "ADD_YOUR_KEY_HERE":
                print(f"✅ {name:12} : {self.mask_key(key)}")
            else:
                print(f"❌ {name:12} : Not configured")
        
        available = self.get_available_providers()
        print("-" * 60)
        print(f"Total configured: {len(available)}/{len(providers)}")
        
        if available:
            print(f"Primary provider: {self.get_primary_provider()}")


class MultiProviderClient:
    """
    Manage multiple AI provider clients with automatic fallback
    """
    def __init__(self, config: APIConfig):
        self.config = config
        self.clients = {}
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize available clients based on configured keys"""
        
        # OpenAI
        if self.config.openai_key:
            try:
                from openai import OpenAI
                self.clients["openai"] = OpenAI(api_key=self.config.openai_key)
                print("✅ OpenAI client initialized")
            except ImportError:
                print("⚠️ OpenAI package not installed. Run: pip install openai")
        
        # Anthropic
        if self.config.anthropic_key:
            try:
                from anthropic import Anthropic
                self.clients["anthropic"] = Anthropic(api_key=self.config.anthropic_key)
                print("✅ Anthropic client initialized")
            except ImportError:
                print("⚠️ Anthropic package not installed. Run: pip install anthropic")
        
        # Google
        if self.config.google_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.config.google_key)
                self.clients["google"] = genai
                print("✅ Google Gemini client initialized")
            except ImportError:
                print("⚠️ Google package not installed. Run: pip install google-generativeai")
    
    def get_client(self, provider: str = None):
        """Get a specific client or the first available one"""
        if provider:
            return self.clients.get(provider)
        
        # Return first available client
        for provider, client in self.clients.items():
            return client
        
        return None
    
    def list_available_models(self) -> Dict[str, List[str]]:
        """List available models for each configured provider"""
        models = {}
        
        if "openai" in self.clients:
            models["openai"] = [
                "gpt-3.5-turbo",
                "gpt-4",
                "gpt-4-turbo-preview"
            ]
        
        if "anthropic" in self.clients:
            models["anthropic"] = [
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307"
            ]
        
        if "google" in self.clients:
            models["google"] = [
                "gemini-pro",
                "gemini-pro-vision"
            ]
        
        return models


def create_example_config_files():
    """Create example configuration files for users to customize"""
    
    # Create config.example.json
    example_config = {
        "openai_key": "ADD_YOUR_KEY_HERE",
        "anthropic_key": "ADD_YOUR_KEY_HERE",
        "google_key": "ADD_YOUR_KEY_HERE",
        "replicate_key": "ADD_YOUR_KEY_HERE",
        "default_temperature": 0.7,
        "max_tokens": 500,
        "timeout": 30
    }
    
    with open("config.example.json", "w") as f:
        json.dump(example_config, f, indent=2)
    
    print("✅ Created config.example.json")
    
    # Create .env.example
    env_example = """# API Keys Configuration
# Copy this file to .env and add your actual keys

# OpenAI API Key (https://platform.openai.com/api-keys)
OPENAI_API_KEY=ADD_YOUR_KEY_HERE

# Anthropic API Key (https://console.anthropic.com/)
ANTHROPIC_API_KEY=ADD_YOUR_KEY_HERE

# Google AI Studio Key (https://aistudio.google.com/)
GOOGLE_API_KEY=ADD_YOUR_KEY_HERE

# Replicate API Token (https://replicate.com/account/api-tokens)
REPLICATE_API_TOKEN=ADD_YOUR_KEY_HERE
"""
    
    with open(".env.example", "w") as f:
        f.write(env_example)
    
    print("✅ Created .env.example")


if __name__ == "__main__":
    # Demonstrate the configuration manager
    print("API Configuration Manager Demo")
    print("=" * 60)
    
    # Load configuration from environment
    config = APIConfig.from_env()
    
    # Display status
    config.display_status()
    
    # Validate configuration
    print("\n" + "=" * 60)
    if config.validate():
        print("\n🎉 Ready to use AI APIs!")
        
        # Initialize multi-provider client
        client_manager = MultiProviderClient(config)
        
        # Show available models
        models = client_manager.list_available_models()
        if models:
            print("\nAvailable models:")
            for provider, model_list in models.items():
                print(f"\n{provider}:")
                for model in model_list:
                    print(f"  - {model}")
    else:
        print("\n📝 To get started:")
        print("1. Copy .env.example to .env")
        print("2. Add your API keys")
        print("3. Run this script again")
        
        # Create example files if they don't exist
        if not os.path.exists(".env.example"):
            print("\nCreating example configuration files...")
            create_example_config_files()
