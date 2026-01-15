# Save as: api_key_manager.py
"""
Secure API key management for AI agent services.
Keys are hashed before storage - never stored in plain text.
"""

import secrets
import hashlib
from datetime import datetime
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader


class APIKeyManager:
    """Manage API keys securely."""
    
    def __init__(self):
        # Store hashed keys, not plain text
        self.keys: dict = {}  # hash -> metadata
    
    def generate_key(self, user_id: str) -> str:
        """
        Generate a new API key.
        
        Returns the key ONCE - user must save it.
        We only store the hash, so we can't recover it later.
        """
        # Generate a secure random key
        key = f"sk_{secrets.token_urlsafe(32)}"
        
        # Store only the hash
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        self.keys[key_hash] = {
            "user_id": user_id,
            "created": datetime.now().isoformat(),
            "last_used": None
        }
        
        # Return the key ONCE - user must save it
        return key
    
    def verify_key(self, key: str) -> dict | None:
        """
        Verify an API key and return its metadata.
        
        Returns None if key is invalid.
        """
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        if key_hash in self.keys:
            # Update last used
            self.keys[key_hash]["last_used"] = datetime.now().isoformat()
            return self.keys[key_hash]
        
        return None
    
    def revoke_key(self, key: str) -> bool:
        """Revoke an API key."""
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        if key_hash in self.keys:
            del self.keys[key_hash]
            return True
        return False
    
    def list_keys_for_user(self, user_id: str) -> list:
        """List metadata for all keys belonging to a user."""
        return [
            {**meta, "hash_prefix": h[:8]}
            for h, meta in self.keys.items()
            if meta["user_id"] == user_id
        ]


# Global key manager instance
key_manager = APIKeyManager()

# FastAPI security setup
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)) -> dict:
    """
    Verify the API key and return user info.
    
    Use as a FastAPI dependency for protected endpoints.
    """
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key required",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    user_info = key_manager.verify_key(api_key)
    if not user_info:
        # Don't reveal whether key exists or is wrong format
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    return user_info


# Example FastAPI app
app = FastAPI(title="Secure API Key Demo")


@app.post("/admin/keys")
async def create_key(user_id: str):
    """
    Create a new API key for a user.
    
    In production, this endpoint should be admin-only.
    """
    key = key_manager.generate_key(user_id)
    return {
        "key": key,
        "message": "Save this key - it cannot be retrieved later!"
    }


@app.get("/protected")
async def protected_endpoint(user: dict = Security(verify_api_key)):
    """Example protected endpoint."""
    return {
        "message": "Access granted!",
        "user_id": user["user_id"]
    }


@app.delete("/admin/keys/{user_id}")
async def revoke_user_keys(user_id: str):
    """Revoke all keys for a user."""
    # In production, implement proper key revocation
    return {"message": f"Keys for {user_id} revoked"}


# For production, consider:
# - OAuth 2.0 — For user-facing applications
# - JWT tokens — For stateless authentication  
# - API key rotation — Automated periodic rotation
# - Scoped permissions — Different keys for different access levels


if __name__ == "__main__":
    # Demo
    print("API Key Manager Demo")
    print("=" * 50)
    
    # Generate a key
    key = key_manager.generate_key("user123")
    print(f"\nGenerated key: {key}")
    print("(In production, show this ONCE to the user)")
    
    # Verify it
    result = key_manager.verify_key(key)
    print(f"\nVerification result: {result}")
    
    # Try invalid key
    result = key_manager.verify_key("sk_invalid_key")
    print(f"\nInvalid key result: {result}")
    
    # List user's keys
    keys = key_manager.list_keys_for_user("user123")
    print(f"\nUser's keys (metadata only): {keys}")
    
    print("\n" + "=" * 50)
    print("Run with: uvicorn api_key_manager:app --reload")
