# From: Zero to AI Agent, Chapter 7, Section 7.6
# File: exercise_1_7_6_solution.py

"""
Exercise 1 Solution: Secure Key Storage
A complete key management system with multiple sources, validation, and security.
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, List
from dotenv import load_dotenv
import hashlib
from datetime import datetime


class SecureKeyManager:
    """
    Complete key management system that:
    - Loads keys from multiple sources
    - Validates key format
    - Provides fallback options
    - Never exposes keys in logs or errors
    """
    
    def __init__(self, config_dir: str = "."):
        """Initialize the secure key manager"""
        self.config_dir = Path(config_dir)
        self.keys = {}
        self.key_sources = {}
        self.validation_errors = []
        self._load_all_keys()
    
    def _load_all_keys(self):
        """Load keys from all available sources in priority order"""
        # Priority order: Environment > .env > config.json
        
        # 1. Try environment variables first (highest priority)
        self._load_from_environment()
        
        # 2. Try .env file
        self._load_from_dotenv()
        
        # 3. Try config.json (lowest priority)
        self._load_from_config()
        
        # Validate all loaded keys
        self._validate_all_keys()
    
    def _load_from_environment(self):
        """Load keys directly from environment variables"""
        env_keys = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "google": "GOOGLE_API_KEY",
            "replicate": "REPLICATE_API_TOKEN"
        }
        
        for provider, env_var in env_keys.items():
            key = os.environ.get(env_var)
            if key and key != "ADD_YOUR_KEY_HERE":
                self.keys[provider] = key
                self.key_sources[provider] = "environment"
    
    def _load_from_dotenv(self):
        """Load keys from .env file"""
        env_file = self.config_dir / ".env"
        
        if env_file.exists():
            # Load .env file
            load_dotenv(env_file)
            
            # Check for keys not already loaded
            env_keys = {
                "openai": "OPENAI_API_KEY",
                "anthropic": "ANTHROPIC_API_KEY",
                "google": "GOOGLE_API_KEY",
                "replicate": "REPLICATE_API_TOKEN"
            }
            
            for provider, env_var in env_keys.items():
                if provider not in self.keys:
                    key = os.getenv(env_var)
                    if key and key != "ADD_YOUR_KEY_HERE":
                        self.keys[provider] = key
                        self.key_sources[provider] = ".env"
    
    def _load_from_config(self):
        """Load keys from config.json file"""
        config_file = self.config_dir / "config.json"
        
        if config_file.exists():
            try:
                with open(config_file) as f:
                    config = json.load(f)
                
                # Map config keys to providers
                config_map = {
                    "openai": "openai_key",
                    "anthropic": "anthropic_key",
                    "google": "google_key",
                    "replicate": "replicate_key"
                }
                
                for provider, config_key in config_map.items():
                    if provider not in self.keys:
                        key = config.get(config_key)
                        if key and key != "ADD_YOUR_KEY_HERE":
                            self.keys[provider] = key
                            self.key_sources[provider] = "config.json"
            
            except json.JSONDecodeError as e:
                self.validation_errors.append(f"Invalid config.json: {e}")
    
    def _validate_all_keys(self):
        """Validate format of all loaded keys"""
        validation_rules = {
            "openai": {
                "prefix": "sk-",
                "min_length": 20,
                "pattern": r'^sk-[a-zA-Z0-9]{20,}$'
            },
            "anthropic": {
                "prefix": "sk-ant-",
                "min_length": 20,
                "pattern": r'^sk-ant-[a-zA-Z0-9-]+$'
            },
            "google": {
                "prefix": "AIza",
                "min_length": 30,
                "pattern": r'^AIza[a-zA-Z0-9_-]{35}$'
            },
            "replicate": {
                "prefix": None,  # No specific prefix
                "min_length": 40,
                "pattern": r'^[a-f0-9]{40}$'
            }
        }
        
        for provider, key in self.keys.items():
            rules = validation_rules.get(provider, {})
            
            # Check prefix
            if rules.get("prefix") and not key.startswith(rules["prefix"]):
                self.validation_errors.append(
                    f"{provider}: Invalid key format (wrong prefix)"
                )
            
            # Check length
            min_length = rules.get("min_length", 20)
            if len(key) < min_length:
                self.validation_errors.append(
                    f"{provider}: Key too short (min {min_length} chars)"
                )
            
            # Check for common mistakes
            if " " in key:
                self.validation_errors.append(
                    f"{provider}: Key contains spaces (copy/paste error?)"
                )
            
            if "\n" in key or "\r" in key:
                self.validation_errors.append(
                    f"{provider}: Key contains newlines (copy/paste error?)"
                )
    
    def get_key(self, provider: str) -> Optional[str]:
        """
        Get API key for a provider with fallback options
        Never exposes the actual key in logs or errors
        """
        if provider in self.keys:
            return self.keys[provider]
        
        # Try alternative names
        alternatives = {
            "gemini": "google",
            "claude": "anthropic",
            "gpt": "openai"
        }
        
        alt_provider = alternatives.get(provider)
        if alt_provider and alt_provider in self.keys:
            return self.keys[alt_provider]
        
        return None
    
    def get_masked_key(self, provider: str) -> str:
        """Get a masked version of the key for display"""
        key = self.get_key(provider)
        
        if not key:
            return "Not configured"
        
        if len(key) < 10:
            return "Invalid"
        
        # Show first 7 and last 4 characters only
        return f"{key[:7]}...{key[-4:]}"
    
    def get_key_hash(self, provider: str) -> Optional[str]:
        """Get SHA-256 hash of key for comparison without exposing it"""
        key = self.get_key(provider)
        
        if not key:
            return None
        
        return hashlib.sha256(key.encode()).hexdigest()
    
    def is_configured(self, provider: str) -> bool:
        """Check if a provider is configured"""
        return provider in self.keys
    
    def get_configured_providers(self) -> List[str]:
        """Get list of configured providers"""
        return list(self.keys.keys())
    
    def get_status_report(self) -> Dict:
        """Get detailed status report without exposing keys"""
        return {
            "configured_providers": self.get_configured_providers(),
            "total_configured": len(self.keys),
            "sources": {
                provider: source 
                for provider, source in self.key_sources.items()
            },
            "validation_errors": self.validation_errors,
            "is_valid": len(self.validation_errors) == 0
        }
    
    def safe_log_status(self):
        """Log status information without exposing sensitive data"""
        print("=" * 60)
        print("🔐 Secure Key Manager Status")
        print("=" * 60)
        
        status = self.get_status_report()
        
        # Show configured providers
        if status["configured_providers"]:
            print(f"\n✅ Configured Providers ({status['total_configured']}):")
            for provider in status["configured_providers"]:
                source = status["sources"][provider]
                masked = self.get_masked_key(provider)
                print(f"  • {provider}: {masked} (from {source})")
        else:
            print("\n❌ No providers configured")
        
        # Show validation errors
        if status["validation_errors"]:
            print(f"\n⚠️ Validation Errors:")
            for error in status["validation_errors"]:
                print(f"  • {error}")
        
        # Never log actual keys!
        print("\n💡 Keys are loaded and validated but never exposed in logs")
    
    def export_safe_config(self, filepath: str = "config.safe.json"):
        """Export configuration info without exposing keys"""
        safe_config = {
            "timestamp": datetime.now().isoformat(),
            "providers": {}
        }
        
        for provider in self.keys:
            safe_config["providers"][provider] = {
                "configured": True,
                "source": self.key_sources.get(provider),
                "key_hash": self.get_key_hash(provider),
                "masked_key": self.get_masked_key(provider)
            }
        
        with open(filepath, "w") as f:
            json.dump(safe_config, f, indent=2)
        
        print(f"✅ Safe configuration exported to {filepath}")


# Example usage and testing
if __name__ == "__main__":
    print("Secure Key Management System Demo")
    print("=" * 60)
    
    # Create the secure key manager
    manager = SecureKeyManager()
    
    # Display safe status
    manager.safe_log_status()
    
    # Test key retrieval with fallback
    print("\n" + "=" * 60)
    print("Testing Key Retrieval with Fallback")
    print("=" * 60)
    
    test_providers = ["openai", "gpt", "claude", "anthropic", "gemini", "google"]
    
    for provider in test_providers:
        if manager.is_configured(provider):
            masked = manager.get_masked_key(provider)
            print(f"✅ {provider}: {masked}")
        else:
            # Try fallback
            key = manager.get_key(provider)
            if key:
                print(f"✅ {provider}: Found via fallback")
            else:
                print(f"❌ {provider}: Not configured")
    
    # Export safe configuration
    print("\n" + "=" * 60)
    manager.export_safe_config()
    
    print("\n✅ Secure Key Manager initialized successfully!")
    print("   • Keys are loaded from multiple sources")
    print("   • All keys are validated")
    print("   • Fallback options are available")
    print("   • Keys are never exposed in logs or errors")
