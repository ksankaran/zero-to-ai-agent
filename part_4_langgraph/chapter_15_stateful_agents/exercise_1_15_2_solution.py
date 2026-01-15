# From: Zero to AI Agent, Chapter 15, Section 15.2
# File: exercise_1_15_2_solution.py

"""
Validated user profile with Pydantic.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum
import re

class MembershipLevel(str, Enum):
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"

class UserProfile(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: str
    age: Optional[int] = Field(default=None, ge=13, le=120)
    membership: MembershipLevel = MembershipLevel.FREE
    
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9]+$', v):
            raise ValueError('Username must be alphanumeric')
        return v.lower()
    
    @field_validator('email')
    @classmethod
    def email_valid(cls, v):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', v):
            raise ValueError('Invalid email format')
        return v.lower()

# Test valid profiles
print("=== Valid Profiles ===")
valid = UserProfile(username="Alice123", email="alice@test.com", age=25)
print(f"✓ {valid.username}, {valid.email}, {valid.membership.value}")

minimal = UserProfile(username="bob", email="bob@test.com")
print(f"✓ {minimal.username}, age={minimal.age}")

# Test invalid profiles
print("\n=== Invalid Profiles ===")
test_cases = [
    ({"username": "ab", "email": "a@b.com"}, "too short"),
    ({"username": "test_user", "email": "a@b.com"}, "underscore"),
    ({"username": "test", "email": "notanemail"}, "bad email"),
    ({"username": "test", "email": "a@b.com", "age": 10}, "too young"),
]

for data, reason in test_cases:
    try:
        UserProfile(**data)
        print(f"✗ Should have failed: {reason}")
    except Exception as e:
        print(f"✓ Caught ({reason})")
