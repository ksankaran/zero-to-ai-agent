# From: Zero to AI Agent, Chapter 19, Section 19.3
# File: exercise_2_19_3_solution.py (config.py)
# Description: Robust configuration system for local and production environments

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """Application configuration with validation."""
    
    # Required settings (no defaults)
    openai_api_key: str
    
    # Optional settings with defaults
    api_key: str = "dev-key-change-in-production"
    debug: bool = False
    log_level: str = "INFO"
    port: int = 8000
    model_name: str = "gpt-3.5-turbo"
    max_tokens: int = 1000
    
    @classmethod
    def from_environment(cls) -> "Config":
        """Load configuration from environment variables."""
        
        # Try to load .env file in development
        env_file = Path(".env")
        if env_file.exists():
            cls._load_env_file(env_file)
        
        # Validate required settings
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ConfigurationError(
                "OPENAI_API_KEY is required. "
                "Set it in your .env file (local) or platform environment variables (production)."
            )
        
        # Build config with environment values or defaults
        return cls(
            openai_api_key=openai_key,
            api_key=os.getenv("API_KEY", cls.api_key),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", cls.log_level),
            port=int(os.getenv("PORT", cls.port)),
            model_name=os.getenv("MODEL_NAME", cls.model_name),
            max_tokens=int(os.getenv("MAX_TOKENS", cls.max_tokens)),
        )
    
    @staticmethod
    def _load_env_file(path: Path) -> None:
        """Load environment variables from a .env file."""
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    # Don't override existing environment variables
                    if key not in os.environ:
                        os.environ[key] = value


class ConfigurationError(Exception):
    """Raised when required configuration is missing."""
    pass


# Usage in your application
def create_app():
    """Create the FastAPI application with validated config."""
    from fastapi import FastAPI
    
    try:
        config = Config.from_environment()
    except ConfigurationError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nRequired environment variables:")
        print("  - OPENAI_API_KEY: Your OpenAI API key")
        print("\nOptional environment variables:")
        print("  - API_KEY: API key for authentication (default: dev-key-change-in-production)")
        print("  - DEBUG: Enable debug mode (default: false)")
        print("  - LOG_LEVEL: Logging level (default: INFO)")
        print("  - PORT: Server port (default: 8000)")
        print("  - MODEL_NAME: OpenAI model to use (default: gpt-3.5-turbo)")
        print("  - MAX_TOKENS: Maximum tokens per response (default: 1000)")
        raise SystemExit(1)
    
    # Now use config throughout your app
    app = FastAPI(debug=config.debug)
    
    # Example: using config in an endpoint
    @app.get("/config/info")
    def config_info():
        """Return non-sensitive configuration info."""
        return {
            "debug": config.debug,
            "log_level": config.log_level,
            "model_name": config.model_name,
            "max_tokens": config.max_tokens,
            # Never expose API keys!
        }
    
    return app, config
